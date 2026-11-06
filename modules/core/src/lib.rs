//! Composition root: owns adapters via contracts, not concrete crates.
use nolp_contracts::{normalized_dns_host, Decision, Module, ModuleState, Policy, Request, Verdict};
use std::collections::HashSet;

/// Runtime admission of independently implemented modules.
/// A declared scaffold is never an operational capability.
pub struct ModuleRegistry {
    ids: HashSet<&'static str>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum RegistrationError {
    NotReady,
    DuplicateId,
}

impl ModuleRegistry {
    pub fn new() -> Self {
        Self {
            ids: HashSet::new(),
        }
    }

    pub fn register(&mut self, module: &dyn Module) -> Result<(), RegistrationError> {
        if module.state() != ModuleState::Ready {
            return Err(RegistrationError::NotReady);
        }
        if !self.ids.insert(module.id()) {
            return Err(RegistrationError::DuplicateId);
        }
        Ok(())
    }

    pub fn contains(&self, id: &str) -> bool {
        self.ids.contains(id)
    }
}

impl Default for ModuleRegistry {
    fn default() -> Self {
        Self::new()
    }
}

pub struct PolicyChain {
    policies: Vec<Box<dyn Policy>>,
}
impl PolicyChain {
    pub fn new() -> Self {
        Self { policies: Vec::new() }
    }
    pub fn add(&mut self, policy: impl Policy + 'static) {
        self.policies.push(Box::new(policy));
    }
    pub fn evaluate(&self, request: &Request<'_>) -> Verdict {
        if normalized_dns_host(request.host).is_none() {
            return Verdict {
                decision: Decision::Block,
                reason: "invalid-dns-host",
            };
        }
        for policy in &self.policies {
            let verdict = policy.evaluate(request);
            if verdict.decision == Decision::Block {
                return verdict;
            }
        }
        Verdict {
            decision: Decision::Allow,
            reason: "no-blocking-policy",
        }
    }
}
impl Default for PolicyChain {
    fn default() -> Self {
        Self::new()
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    struct ExampleModule {
        state: ModuleState,
    }
    impl Module for ExampleModule {
        fn id(&self) -> &'static str {
            "example"
        }
        fn state(&self) -> ModuleState {
            self.state
        }
    }
    #[test]
    fn registry_rejects_scaffolds_and_duplicates() {
        let mut registry = ModuleRegistry::new();
        assert_eq!(
            registry.register(&ExampleModule {
                state: ModuleState::Scaffold,
            }),
            Err(RegistrationError::NotReady)
        );
        assert!(!registry.contains("example"));
        assert_eq!(
            registry.register(&ExampleModule {
                state: ModuleState::Ready,
            }),
            Ok(())
        );
        assert!(registry.contains("example"));
        assert_eq!(
            registry.register(&ExampleModule {
                state: ModuleState::Ready,
            }),
            Err(RegistrationError::DuplicateId)
        );
    }
    struct Block;
    impl Policy for Block {
        fn evaluate(&self, _: &Request<'_>) -> Verdict {
            Verdict {
                decision: Decision::Block,
                reason: "test",
            }
        }
    }
    #[test]
    fn invalid_host_fails_closed() {
        let chain = PolicyChain::new();
        for host in ["", "https://example.com", "a..b", "127.0.0.1"] {
            assert_eq!(
                chain.evaluate(&Request {
                    host,
                    private: false,
                })
                .decision,
                Decision::Block
            );
        }
    }
    #[test]
    fn compose_policy() {
        let mut chain = PolicyChain::new();
        chain.add(Block);
        assert_eq!(
            chain
                .evaluate(&Request {
                    host: "example.org",
                    private: false,
                })
                .decision,
            Decision::Block
        );
    }
}
