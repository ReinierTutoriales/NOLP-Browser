//! Consent gate only; no Mozilla Account or Sync integration.
use nolp_contracts::{Module,ModuleState};
pub struct FirefoxAccount { pub consent: bool }
impl Default for FirefoxAccount { fn default()->Self {Self{consent:false}} }
impl Module for FirefoxAccount {fn id(&self)->&'static str{"identity-firefox"} fn state(&self)->ModuleState{ModuleState::RequiresConsent}}
#[cfg(test)] mod tests {use super::*;#[test] fn no_default_consent(){assert!(!FirefoxAccount::default().consent);}}
