//! Media capability placeholder. No codecs or playback implemented.
use nolp_contracts::{Module,ModuleState};
pub struct MediaUnavailable;
impl Module for MediaUnavailable {fn id(&self)->&'static str{"media"} fn state(&self)->ModuleState{ModuleState::Unavailable}}
