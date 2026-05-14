import os

from power_system_inertia.base import PowerSystemInertiaBase
from power_system_inertia.slides.slide_01_balance import slide as slide_01_balance
from power_system_inertia.slides.slide_02_disturbance import slide as slide_02_disturbance
from power_system_inertia.slides.slide_03_kinetic_energy import slide as slide_03_kinetic_energy
from power_system_inertia.slides.slide_04_swing_equation import slide as slide_04_swing_equation
from power_system_inertia.slides.slide_05_inertia_constant import slide as slide_05_inertia_constant
from power_system_inertia.slides.slide_06_rocof import slide as slide_06_rocof
from power_system_inertia.slides.slide_07_minimum_inertia import slide as slide_07_minimum_inertia
from power_system_inertia.slides.slide_08_angular_stability import slide as slide_08_angular_stability
from power_system_inertia.slides.slide_09_synthetic_inertia_grid_forming import slide as slide_09_synthetic_inertia_grid_forming
from power_system_inertia.slides.slide_10_hsys_reduction_example import slide as slide_10_hsys_reduction_example
from power_system_inertia.slides.slide_11_nadir_vs_rocof import slide as slide_11_nadir_vs_rocof
from power_system_inertia.slides.slide_12_damping_appendix import slide as slide_12_damping_appendix
from power_system_inertia.slides.slide_13_summary import slide as slide_13_summary


# Change this flag to "pt", "en", "de", or "zh".
# The MANIM_LANGUAGE environment variable can override it for one render.
LANGUAGE = os.environ.get("MANIM_LANGUAGE", "pt")

SLIDE_SEQUENCE = [
    slide_01_balance,
    slide_02_disturbance,
    slide_03_kinetic_energy,
    slide_04_swing_equation,
    slide_05_inertia_constant,
    slide_06_rocof,
    slide_07_minimum_inertia,
    slide_08_angular_stability,
    slide_09_synthetic_inertia_grid_forming,
    slide_10_hsys_reduction_example,
    slide_11_nadir_vs_rocof,
    slide_12_damping_appendix,
    slide_13_summary,
]


class PowerSystemInertiaStability(PowerSystemInertiaBase):
    def construct(self):
        self.setup_scene(language_code=LANGUAGE)
        for slide_module in SLIDE_SEQUENCE:
            slide_module.play(self)
