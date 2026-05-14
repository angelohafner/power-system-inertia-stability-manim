"""Language dictionary for the Manim animation.

The slide code uses exact Portuguese text as dictionary keys. Missing
translations intentionally fall back to Portuguese so a partially translated
language can still render while new entries are added.
"""

EN = {
    "Equilíbrio entre geração e carga": "Balance Between Generation and Load",
    "Em regime permanente, a frequência permanece estável quando a\npotência gerada equilibra a potência consumida mais as perdas.": (
        "At steady state, frequency remains stable when\n"
        "generated power balances load plus losses."
    ),
    r"P_{\text{geração}}": r"P_{\text{generation}}",
    r"P_{\text{carga}}": r"P_{\text{load}}",
    r"P_{\text{perdas}}": r"P_{\text{losses}}",
    "(desprezando perdas internas do gerador)": "(neglecting internal generator losses)",
    "Desequilíbrio de potência": "Power Imbalance",
    "excursão transitória (resposta inercial) — não é regime permanente": (
        "transient excursion (inertial response) -- not steady state"
    ),
    "Quando a carga supera a geração,": "When load exceeds generation,",
    "o sistema precisa retirar energia": "the system must draw energy",
    "de algum lugar nos primeiros instantes.": "from somewhere in the first instants.",
    "Energia cinética e inércia": "Kinetic Energy and Inertia",
    "O rotor das máquinas síncronas armazena energia cinética.": (
        "The rotor of synchronous machines stores kinetic energy."
    ),
    "A inércia não impede a queda de frequência, mas reduz a rapidez dessa queda.": (
        "Inertia does not prevent the frequency drop, but it reduces how fast it falls."
    ),
    "resposta inicial": "initial response",
    r"J_m:\ \text{momento de inércia mecânico }[\mathrm{kg\,m^2}]": (
        r"J_m:\ \text{mechanical moment of inertia }[\mathrm{kg\,m^2}]"
    ),
    r"\omega_m:\ \text{velocidade angular mecânica }[\mathrm{rad/s}]": (
        r"\omega_m:\ \text{mechanical angular speed }[\mathrm{rad/s}]"
    ),
    r"E_k:\ \text{energia cinética armazenada }[\mathrm{J}]": (
        r"E_k:\ \text{stored kinetic energy }[\mathrm{J}]"
    ),
    "Equação de oscilação": "Swing Equation",
    "(a) Forma em torque, fisicamente exata:": "(a) Torque form, physically exact:",
    r"(b) Forma em potência, válida para $\omega_m \approx \omega_{0,m}$:": (
        r"(b) Power form, valid for $\omega_m \approx \omega_{0,m}$:"
    ),
    "(c) Forma normalizada em pu:": "(c) Per-unit normalized form:",
    r"T:\ \text{torque }[\mathrm{N\cdot m}]": r"T:\ \text{torque }[\mathrm{N\cdot m}]",
    r"P:\ \text{potência }[\mathrm{W}\ \text{ou } \mathrm{pu}]": (
        r"P:\ \text{power }[\mathrm{W}\ \text{or } \mathrm{pu}]"
    ),
    r"D_m:\ \text{amortecimento mecânico }[\mathrm{N\cdot m\cdot s/rad}]": (
        r"D_m:\ \text{mechanical damping }[\mathrm{N\cdot m\cdot s/rad}]"
    ),
    r"D_g:\ \text{amortecimento em potência }[\mathrm{W\cdot s/rad}]": (
        r"D_g:\ \text{power damping }[\mathrm{W\cdot s/rad}]"
    ),
    r"D_{pu}:\ \text{amortecimento normalizado }[\mathrm{pu/pu}]": (
        r"D_{pu}:\ \text{normalized damping }[\mathrm{pu/pu}]"
    ),
    r"D_{pu}:\ \text{frequentemente tratado como adimensional na prática}": (
        r"D_{pu}:\ \text{often treated as dimensionless in practice}"
    ),
    "Frequência e constante de inércia": "Frequency and Inertia Constant",
    r"J_m:\ \text{momento de inércia mecânico }[\mathrm{kg\,m^2}]": (
        r"J_m:\ \text{mechanical moment of inertia }[\mathrm{kg\,m^2}]"
    ),
    r"H:\ \text{constante de inércia em pu }[\mathrm{s}]": (
        r"H:\ \text{per-unit inertia constant }[\mathrm{s}]"
    ),
    r"\quad \text{energia cinética nominal}/S_{base}": (
        r"\quad \text{rated kinetic energy}/S_{base}"
    ),
    r"S_{base}:\ \text{potência aparente base }[\mathrm{VA\ ou\ MVA}]": (
        r"S_{base}:\ \text{base apparent power }[\mathrm{VA\ or\ MVA}]"
    ),
    r"\omega_{0,m},\omega_0:\ \text{velocidades nominais }[\mathrm{rad/s}]": (
        r"\omega_{0,m},\omega_0:\ \text{rated speeds }[\mathrm{rad/s}]"
    ),
    r"M=\frac{2H}{\omega_0}:\ \text{constante de partida }[\mathrm{s^2}]": (
        r"M=\frac{2H}{\omega_0}:\ \text{starting constant }[\mathrm{s^2}]"
    ),
    r"H_{sys}:\ \text{inércia equivalente do sistema }[\mathrm{s}]": (
        r"H_{sys}:\ \text{equivalent system inertia }[\mathrm{s}]"
    ),
    "Quanto maior a inércia equivalente": "The larger the equivalent inertia",
    "menor o módulo da taxa inicial de variação da frequência.": (
        "the smaller the magnitude of the initial rate of change of frequency."
    ),
    r"H_{sys}\ \text{baixo}": r"H_{sys}\ \text{low}",
    r"H_{sys}\ \text{alto}": r"H_{sys}\ \text{high}",
    "(Rate of Change of Frequency - Taxa de Variação de Frequência)": (
        "(Rate of Change of Frequency)"
    ),
    "para a mesma perturbação": "for the same disturbance",
    "Baixa inércia causa maior RoCoF.": "Low inertia causes higher RoCoF.",
    "Condição mínima de inércia": "Minimum Inertia Condition",
    "Essa inequação representa a inércia mínima necessária\npara limitar a variação brusca da frequência.": (
        "This inequality represents the minimum inertia required\n"
        "to limit abrupt frequency variation."
    ),
    "Substituir geradores síncronos por inversores fotovoltaicos/eólicos": (
        "Replacing synchronous generators with photovoltaic/wind inverters"
    ),
    r"($H \approx 0$ com $S$ não-nulo) reduz $H_{sys}$ e aumenta RoCoF.": (
        r"($H \approx 0$ with nonzero $S$) reduces $H_{sys}$ and increases RoCoF."
    ),
    "região crítica": "critical region",
    "região segura": "safe region",
    "Estabilidade angular": "Angular Stability",
    "A inércia reduz a rapidez da variação da frequência.": (
        "Inertia reduces how fast frequency changes."
    ),
    "A estabilidade também depende do amortecimento": "Stability also depends on damping",
    "e do sincronismo elétrico.": "and electrical synchronism.",
    r"Conforme o sistema é mais carregado ($\delta_0$ cresce),": (
        r"As the system becomes more heavily loaded ($\delta_0$ increases),"
    ),
    r"$K_s$ diminui e a margem de estabilidade encolhe.": (
        r"$K_s$ decreases and the stability margin shrinks."
    ),
    "Instabilidade transitória:": "Transient instability:",
    "perda de sincronismo": "loss of synchronism",
    r"Após uma falta severa, $\delta$ pode crescer": (
        r"After a severe fault, $\delta$ can grow"
    ),
    "monotonicamente, sem oscilar em torno do equilíbrio.": (
        "monotonically, without oscillating around equilibrium."
    ),
    "Para análise transitória usa-se o método das áreas iguais": (
        "For transient analysis, use the Equal Area Criterion"
    ),
    "(Equal Area Criterion) ou simulação no domínio do tempo,": (
        "or time-domain simulation,"
    ),
    "não o autovalor da equação linearizada.": (
        "not the eigenvalue of the linearized equation."
    ),
    r"M:\ \text{constante de partida }[\mathrm{s^2}]": (
        r"M:\ \text{starting constant }[\mathrm{s^2}]"
    ),
    r"D:\ \text{amortecimento }[\mathrm{pu\cdot s/rad}]": (
        r"D:\ \text{damping }[\mathrm{pu\cdot s/rad}]"
    ),
    r"K_s:\ \text{sincronismo elétrico }[\mathrm{pu/rad}]": (
        r"K_s:\ \text{electrical synchronism }[\mathrm{pu/rad}]"
    ),
    r"\delta:\ \text{ângulo elétrico }[\mathrm{rad}]": (
        r"\delta:\ \text{electrical angle }[\mathrm{rad}]"
    ),
    "Inércia sintética e Grid-Forming": "Synthetic Inertia and Grid-Forming",
    "Sistemas modernos têm penetração crescente de inversores.": (
        "Modern systems have increasing inverter penetration."
    ),
    r"\textit{O sinal negativo significa que o inversor injeta potência quando a frequência está caindo, opondo-se à variação.}": (
        r"\textit{The negative sign means the inverter injects power when frequency is falling, opposing the change.}"
    ),
    "Fast Frequency Response (FFR) das baterias atua nos primeiros segundos, complementando (não substituindo) a inércia.": (
        "Battery Fast Frequency Response (FFR) acts in the first seconds, complementing (not replacing) inertia."
    ),
    "segue a frequência da rede": "follows grid frequency",
    "NÃO entrega inércia naturalmente": "does NOT provide inertia naturally",
    "impõe tensão/frequência": "sets voltage/frequency",
    "pode emular inércia por controle": "can emulate inertia by control",
    "GFL pode fazer Fast Frequency Response (FFR), mas depende": (
        "GFL can provide Fast Frequency Response (FFR), but depends"
    ),
    "de PLL e tem delay.": "on a PLL and has delay.",
    "GFM emula comportamento inercial de forma mais natural,": (
        "GFM emulates inertial behavior more naturally,"
    ),
    "sem depender de PLL para seguir uma rede forte.": (
        "without relying on a PLL to follow a strong grid."
    ),
    "Convenção:": "Convention:",
    r"Em Hz (com $\Delta\omega_{pu}=\Delta f/f_0$):": (
        r"In Hz (with $\Delta\omega_{pu}=\Delta f/f_0$):"
    ),
    "síncrona:": "synchronous:",
    "inércia física, instantânea, sem controle": "physical inertia, instantaneous, no control",
    "inversor:": "inverter:",
    "``inércia'' via software, com delay, saturação e energia DC disponível": (
        "``inertia'' through software, with delay, saturation and available DC energy"
    ),
    r"\textbf{Exemplo: redução de }$H_{sys}$": r"\textbf{Example: reduction of }$H_{sys}$",
    r"Mesma capacidade instalada, $H_{sys}$ cai $\sim 3\times$.": (
        r"Same installed capacity, $H_{sys}$ drops by $\sim 3\times$."
    ),
    r"RoCoF para o mesmo $\Delta P$ triplica.": (
        r"RoCoF for the same $\Delta P$ triples."
    ),
    "Nadir de frequência vs RoCoF": "Frequency Nadir vs RoCoF",
    r"R[\mathrm{Hz/pu}],\quad D_f=\frac{\partial P_{carga}}{\partial f}[\mathrm{pu/Hz}]": (
        r"R[\mathrm{Hz/pu}],\quad D_f=\frac{\partial P_{load}}{\partial f}[\mathrm{pu/Hz}]"
    ),
    r"dependendo de $H_{sys}$, $\Delta P$, $R$, $D_f$ e tempo de resposta do governador $T_g$.": (
        r"depending on $H_{sys}$, $\Delta P$, $R$, $D_f$ and governor response time $T_g$."
    ),
    r"Depende de reserva primária, droop $R$ e tempo": (
        r"Depends on primary reserve, droop $R$ and"
    ),
    "da governação e amortecimento da carga.": "governor timing and load damping.",
    r"$\mathrm{RoCoF}$: declividade inicial ($df/dt$ em $t=0^+$).": (
        r"$\mathrm{RoCoF}$: initial slope ($df/dt$ at $t=0^+$)."
    ),
    r"Depende de $H_{sys}$ e $\Delta P$.": r"Depends on $H_{sys}$ and $\Delta P$.",
    "Nadir: frequência mínima atingida durante o transitório.": (
        "Nadir: minimum frequency reached during the transient."
    ),
    r"$\mathrm{UFLS}$ em sistemas 60 Hz: tipicamente 59,5 a 58,5 Hz.": (
        r"$\mathrm{UFLS}$ in 60 Hz systems: typically 59.5 to 58.5 Hz."
    ),
    r"RoCoF depende de $H_{sys}$ e $\Delta P$.": (
        r"RoCoF depends on $H_{sys}$ and $\Delta P$."
    ),
    r"Nadir depende de $H_{sys}$, $\Delta P$, reserva, droop, $D_f$ e dinâmica do governador.": (
        r"Nadir depends on $H_{sys}$, $\Delta P$, reserve, droop, $D_f$ and governor dynamics."
    ),
    r"\textbf{Damping}": r"\textbf{Damping}",
    "No gerador:": "At the generator:",
    r"D_{mec}": r"D_{mech}",
    r"D_{amort}": r"D_{damper}",
    "atrito mecânico + enrolamentos amortecedores": "mechanical friction + damper windings",
    "Na rede:": "At the grid:",
    r"\frac{\partial P_{carga}}{\partial f}": r"\frac{\partial P_{load}}{\partial f}",
    r"\frac{\partial P_{carga}}{\partial f}>0\ \Rightarrow\ \text{carga ajuda a amortecer a queda de frequência}": (
        r"\frac{\partial P_{load}}{\partial f}>0\ \Rightarrow\ \text{load helps damp the frequency drop}"
    ),
    "auto-regulação da carga, tipicamente 1 a 2 \\%/Hz": (
        "load self-regulation, typically 1 to 2 \\%/Hz"
    ),
    "No sistema (após conversão de unidades):": "At the system level (after unit conversion):",
    "Resumo": "Summary",
    r"\text{Sistema estável}": r"\text{Stable system}",
    r"\text{inércia suficiente}": r"\text{sufficient inertia}",
    r"\text{amortecimento suficiente}": r"\text{sufficient damping}",
    r"\text{controle adequado}": r"\text{adequate control}",
    r"\text{Baixa inércia}": r"\text{Low inertia}",
    r"\text{maior RoCoF}": r"\text{higher RoCoF}",
    r"\text{menor tempo para atuação dos controles}": r"\text{less time for control action}",
    r"Inércia $\neq$ resposta primária. Inércia limita o RoCoF; é a reserva primária (governadores e baterias com FFR) que define o nadir.": (
        r"Inertia $\neq$ primary response. Inertia limits RoCoF; primary reserve (governors and batteries with FFR) defines the nadir."
    ),
    "frequência": "frequency",
    "tempo": "time",
    "alta inércia": "high inertia",
    "baixa inércia": "low inertia",
    "Turbina": "Turbine",
    "Gerador": "Generator",
    "Rede": "Grid",
    "Carga": "Load",
    "bem amortecido": "well damped",
    "pouco amortecido": "lightly damped",
    "instável": "unstable",
    "aumento súbito\nde carga": "sudden load\nincrease",
    "referencial síncrono": "synchronous reference",
    "eixo do rotor": "rotor axis",
    "variação angular ligada à velocidade relativa do rotor": (
        "angular variation linked to relative rotor speed"
    ),
    r"$\delta$ é o ângulo elétrico do rotor": r"$\delta$ is the rotor electrical angle",
    "em relação ao referencial síncrono.": "relative to the synchronous reference.",
    r"\text{UFLS }59{,}5\text{ a }58{,}5\ \mathrm{Hz}": (
        r"\text{UFLS }59.5\text{ to }58.5\ \mathrm{Hz}"
    ),
}

LANGUAGES = {
    "pt": {},
    "en": EN,
    # These dictionaries are intentionally ready for progressive completion.
    "de": {
        "Resumo": "Zusammenfassung",
        "frequência": "Frequenz",
        "tempo": "Zeit",
        "Turbina": "Turbine",
        "Gerador": "Generator",
        "Rede": "Netz",
        "Carga": "Last",
        r"\frac{\partial P_{carga}}{\partial f}>0\ \Rightarrow\ \text{carga ajuda a amortecer a queda de frequência}": (
            r"\frac{\partial P_{load}}{\partial f}>0\ \Rightarrow\ \text{Last daempft den Frequenzabfall}"
        ),
    },
    "zh": {
        "Resumo": "总结",
        "frequência": "频率",
        "tempo": "时间",
        "Turbina": "汽轮机",
        "Gerador": "发电机",
        "Rede": "电网",
        "Carga": "负荷",
        r"\frac{\partial P_{carga}}{\partial f}>0\ \Rightarrow\ \text{carga ajuda a amortecer a queda de frequência}": (
            r"\frac{\partial P_{load}}{\partial f}>0\ \Rightarrow\ \text{load damping supports frequency}"
        ),
    },
}
