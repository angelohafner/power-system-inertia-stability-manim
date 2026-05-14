# Power System Inertia Stability - Manim

Animação didática em Manim Community Edition sobre a importância da inércia em sistemas elétricos para estabilidade de frequência e estabilidade angular.

O projeto contém uma cena única, `PowerSystemInertiaStability`, organizada em blocos didáticos que explicam:

- equilíbrio entre geração, carga e perdas;
- desequilíbrio de potência e resposta inercial;
- energia cinética armazenada no rotor;
- equação de oscilação em torque, potência e pu;
- relação entre `H_sys`, RoCoF e frequência;
- condição mínima de inércia;
- estabilidade angular, amortecimento e sincronismo elétrico;
- inércia sintética, Grid-Following, Grid-Forming e FFR;
- diferença entre RoCoF e nadir de frequência.

## Requisitos

- Python 3.10 ou superior
- Manim Community Edition 0.20.1
- NumPy
- LaTeX instalado e acessível no PATH

Instalação mínima:

```powershell
pip install -r requirements.txt
```

## Renderização

Renderizar em 1080p a 30 fps:

```powershell
python -m manim -r 1920,1080 --fps 30 .\power_system_inertia_stability.py PowerSystemInertiaStability
```

Renderizar em 1080p a 60 fps:

```powershell
python -m manim -r 1920,1080 --fps 60 .\power_system_inertia_stability.py PowerSystemInertiaStability
```

## Estrutura modular

Na branch `arquivos-python-separados-por-slide`, o arquivo
`power_system_inertia_stability.py` funciona como arquivo mestre: ele define o
flag `LANGUAGE` e chama os slides na ordem declarada em `SLIDE_SEQUENCE`.

Os helpers compartilhados ficam em `power_system_inertia/base.py`. Cada slide
tem sua própria pasta em `power_system_inertia/slides/`, por exemplo
`slide_01_balance/slide.py`, `slide_02_disturbance/slide.py` e assim por diante.

O dicionário de idiomas fica em `power_system_inertia/languages.py`. O flag pode
ser ajustado para:

- `pt`: português
- `en`: inglês
- `de`: alemão
- `zh`: chinês

Entradas ainda não traduzidas retornam automaticamente ao texto original em
português, permitindo completar a tradução aos poucos.

## Arquivos publicados

Este repositório publica apenas o projeto Python necessário para gerar a animação. Arquivos de vídeo renderizados, previews, caches e saídas locais do Manim são intencionalmente excluídos do versionamento.
