//! Android platform adapter placeholder; GeckoView/Compose not connected.
use nolp_contracts::{Module,ModuleState};
pub struct AndroidUnavailable;
impl Module for AndroidUnavailable {fn id(&self)->&'static str{"platform-android"} fn state(&self)->ModuleState{ModuleState::Unavailable}}
