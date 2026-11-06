//! Conservative local policy for optional remote account services.
use nolp_contracts::{Module, ModuleState};
pub struct Privacy { pub sync_opt_in: bool }
impl Default for Privacy { fn default()->Self { Self { sync_opt_in:false } } }
impl Module for Privacy { fn id(&self)->&'static str { "privacy" } fn state(&self)->ModuleState { ModuleState::Ready } }
#[cfg(test)] mod tests { use super::*; #[test] fn sync_disabled() { assert!(!Privacy::default().sync_opt_in); } }
