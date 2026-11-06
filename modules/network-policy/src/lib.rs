//! Network policy Rust contract. Does not intercept Gecko traffic.
use nolp_contracts::{Decision,Policy,Request,Verdict};
use std::collections::HashSet;
pub struct NetworkPolicy { denied:HashSet<String>, exceptions:HashSet<String> }
impl NetworkPolicy {
    pub fn new(denied:impl IntoIterator<Item=String>, exceptions:impl IntoIterator<Item=String>)->Self {
        Self{denied:denied.into_iter().map(|s|s.to_ascii_lowercase()).collect(),exceptions:exceptions.into_iter().map(|s|s.to_ascii_lowercase()).collect()}
    }
}
impl Policy for NetworkPolicy {
    fn evaluate(&self,request:&Request<'_>)->Verdict {
        let host=request.host.to_ascii_lowercase();
        if self.exceptions.contains(&host) {Verdict{decision:Decision::Allow,reason:"exception"}}
        else if self.denied.contains(&host) {Verdict{decision:Decision::Block,reason:"denied-host"}}
        else {Verdict{decision:Decision::Allow,reason:"no-match"}}
    }
}
#[cfg(test)] mod tests {use super::*;#[test] fn exception_precedence(){let p=NetworkPolicy::new(["example.org".into()],["example.org".into()]);assert_eq!(p.evaluate(&Request{host:"example.org",private:false}).decision,Decision::Allow);}}
