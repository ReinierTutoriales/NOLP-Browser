//! Shared UI theme contract; no renderer yet.
use nolp_contracts::{Surface, Theme};

pub struct AeroSurface {
    theme: Theme,
}
impl AeroSurface {
    pub fn new(theme: Theme) -> Self {
        Self { theme }
    }
}
impl Surface for AeroSurface {
    fn theme(&self) -> Theme {
        self.theme
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn themes() {
        assert_eq!(AeroSurface::new(Theme::AeroDark).theme(), Theme::AeroDark);
    }
}
