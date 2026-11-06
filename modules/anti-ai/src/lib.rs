//! Local explicit host rules only; no general AI detection.
use nolp_contracts::{Decision, Policy, Request, Verdict};
use std::collections::HashSet;
pub struct AntiAi { enabled: bool, hosts: HashSet<String> }
impl AntiAi {
    pub fn new(hosts: impl IntoIterator<Item=String>) -> Self { Self { enabled:true, hosts:hosts.into_iter().map(|h|h.to_ascii_lowercase()).collect() } }
    pub fn set_enabled(&mut self, enabled:bool) { self.enabled=enabled; }
}
impl Policy for AntiAi {
    fn evaluate(&self, request:&Request<'_>)->Verdict {
        if self.enabled && self.hosts.contains(&request.host.to_ascii_lowercase()) { Verdict{decision:Decision::Block,reason:"explicit-ai-host-rule"} }
        else { Verdict{decision:Decision::Allow,reason:"not-blocked"} }
    }
}
#[cfg(test)] mod tests { use super::*; #[test] fn reversible() { let mut a=AntiAi::new(["ai.example".into()]); let r=Request{host:"ai.example",private:false}; assert_eq!(a.evaluate(&r).decision,Decision::Block); a.set_enabled(false); assert_eq!(a.evaluate(&r).decision,Decision::Allow); } }
