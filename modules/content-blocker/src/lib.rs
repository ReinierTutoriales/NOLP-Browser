//! Exact-host prototype only; no real browser interception.
use nolp_contracts::{normalized_dns_host, Decision, Policy, Request, Verdict};
use std::collections::HashSet;

pub struct HostBlocker {
    hosts: HashSet<String>,
}
impl HostBlocker {
    pub fn new(hosts: impl IntoIterator<Item = String>) -> Self {
        Self {
            hosts: hosts.into_iter().filter_map(|h| normalized_dns_host(&h)).collect(),
        }
    }
}
impl Policy for HostBlocker {
    fn evaluate(&self, request: &Request<'_>) -> Verdict {
        if normalized_dns_host(request.host).is_some_and(|host| self.hosts.contains(&host)) {
            Verdict {
                decision: Decision::Block,
                reason: "exact-host-rule",
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
    fn exact_only() {
        let b = HostBlocker::new(["ads.example".into()]);
        assert_eq!(
            b.evaluate(&Request {
                host: "ads.example",
                private: false,
            })
            .decision,
            Decision::Block
        );
        assert_eq!(
            b.evaluate(&Request {
                host: "other.ads.example",
                private: false,
            })
            .decision,
            Decision::Allow
        );
    }
}
