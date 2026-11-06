//! Update capability placeholder. No downloader or signatures implemented.
use nolp_contracts::{Module,ModuleState};
pub struct UpdatesUnavailable;
impl Module for UpdatesUnavailable {fn id(&self)->&'static str{"updates"} fn state(&self)->ModuleState{ModuleState::Unavailable}}
