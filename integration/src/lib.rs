//! Composition smoke: typed module wiring without Gecko integration.
use nolp_anti_ai::AntiAi;
use nolp_content_blocker::HostBlocker;
use nolp_contracts::{Engine, Request, Surface, Theme, Verdict};
use nolp_core::PolicyChain;
use nolp_engine_gecko::GeckoAdapter;
use nolp_network_policy::NetworkPolicy;
use nolp_ui_aero::AeroSurface;

/// Offline policy composition prototype; never intercepts browser traffic.
pub fn evaluate_local(host: &str) -> Verdict {
    let mut chain = PolicyChain::new();
    chain.add(NetworkPolicy::new(["tracker.example".into()], []));
    chain.add(HostBlocker::new(["ads.example".into()]));
    chain.add(AntiAi::new(["ai.example".into()]));
    chain.evaluate(&Request {
        host,
        private: false,
    })
}
/// Production-facing gate: an unintegrated Gecko engine cannot navigate.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum StartupError {
    EngineUnavailable,
}
pub fn start_browser() -> Result<(), StartupError> {
    if integration_ready() {
        Ok(())
    } else {
        Err(StartupError::EngineUnavailable)
    }
}
pub fn integration_ready() -> bool {
    GeckoAdapter::not_integrated().available()
}
pub fn selected_theme() -> Theme {
    AeroSurface::new(Theme::AeroDark).theme()
}

#[cfg(test)]
mod tests {
    use super::*;
    use nolp_contracts::Decision;

    #[test]
    fn invalid_input_is_blocked_before_policy_evaluation() {
        for host in ["", "https://example.com", "a..b", "127.0.0.1"] {
            assert_eq!(evaluate_local(host).decision, Decision::Block);
        }
    }
    #[test]
    fn policy_modules_compose() {
        for host in ["tracker.example", "ads.example", "ai.example"] {
            assert_eq!(evaluate_local(host).decision, Decision::Block);
        }
        assert_eq!(evaluate_local("mozilla.org").decision, Decision::Allow);
    }
    #[test]
    fn no_false_browser_ready() {
        assert!(!integration_ready());
        assert_eq!(start_browser(), Err(StartupError::EngineUnavailable));
        assert_eq!(selected_theme(), Theme::AeroDark);
    }
}
