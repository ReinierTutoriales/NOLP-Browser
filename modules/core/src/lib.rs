//! Composition root: owns adapters via contracts, not concrete crates.
use nolp_contracts::{Decision, Policy, Request, Verdict};

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
