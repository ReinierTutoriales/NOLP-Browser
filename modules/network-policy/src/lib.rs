//! Network policy Rust contract. Does not intercept Gecko traffic.
use nolp_contracts::{normalized_dns_host, Decision, Policy, Request, Verdict};
use std::collections::HashSet;

pub struct NetworkPolicy {
    denied: HashSet<String>,
    exceptions: HashSet<String>,
}
impl NetworkPolicy {
    pub fn new(
        denied: impl IntoIterator<Item = String>,
        exceptions: impl IntoIterator<Item = String>,
    ) -> Self {
        Self {
            denied: denied
                .into_iter()
                .filter_map(|s| normalized_dns_host(&s))
                .collect(),
            exceptions: exceptions
                .into_iter()
                .filter_map(|s| normalized_dns_host(&s))
                .collect(),
        }
    }
}
impl Policy for NetworkPolicy {
    fn evaluate(&self, request: &Request<'_>) -> Verdict {
        let Some(host) = normalized_dns_host(request.host) else {
            return Verdict {
                decision: Decision::Block,
                reason: "invalid-dns-host",
            };
        };
        if self.exceptions.contains(&host) {
            Verdict {
                decision: Decision::Allow,
                reason: "exception",
            }
        } else if self.denied.contains(&host) {
            Verdict {
                decision: Decision::Block,
                reason: "denied-host",
            }
        } else {
            Verdict {
                decision: Decision::Allow,
                reason: "no-match",
            }
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn exception_precedence() {
        let p = NetworkPolicy::new(["example.org".into()], ["example.org".into()]);
        assert_eq!(
            p.evaluate(&Request {
                host: "example.org",
                private: false,
            })
            .decision,
            Decision::Allow
        );
    }
}
