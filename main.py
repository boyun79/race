import json
import math

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="MY F1 GARAGE",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# 차량 성능 데이터
# =========================================================

STATS = [
    "top_speed",
    "acceleration",
    "downforce",
    "grip",
    "stability",
    "braking",
    "cornering",
    "drag",
    "tire_wear",
]

LABELS = {
    "top_speed": "TOP SPEED",
    "acceleration": "ACCELERATION",
    "downforce": "DOWNFORCE",
    "grip": "GRIP",
    "stability": "STABILITY",
    "braking": "BRAKING",
    "cornering": "CORNERING",
    "drag": "DRAG",
    "tire_wear": "TIRE WEAR",
}

HELP = {
    "top_speed": (
        "차량이 직선 구간에서 낼 수 있는 최고 속도입니다. "
        "높을수록 긴 직선에서 유리하지만 다른 성능과의 균형이 중요합니다."
    ),
    "acceleration": (
        "차량이 낮은 속도에서 빠르게 가속하는 능력입니다. "
        "코너 탈출과 직선 진입에서 중요합니다."
    ),
    "downforce": (
        "차량을 노면 방향으로 눌러주는 공기역학적 힘입니다. "
        "높을수록 고속 코너에서 안정적이지만 공기저항도 증가할 수 있습니다."
    ),
    "grip": (
        "타이어가 노면을 붙잡는 능력입니다. "
        "높을수록 코너링과 제동에서 유리합니다."
    ),
    "stability": (
        "차량이 주행 중 얼마나 안정적으로 움직이는지를 나타냅니다. "
        "낮으면 급격한 조작에서 차량이 불안정해질 수 있습니다."
    ),
    "braking": (
        "차량을 빠르고 안정적으로 감속하는 능력입니다. "
        "낮은 속도의 코너에 진입할 때 중요합니다."
    ),
    "cornering": (
        "코너를 빠르게 통과하는 능력입니다. "
        "다운포스, 그립, 차량 밸런스의 영향을 받습니다."
    ),
    "drag": (
        "공기저항의 크기입니다. 낮을수록 직선에서 속도를 내기 쉽지만 "
        "지나치게 낮으면 다운포스가 부족할 수 있습니다."
    ),
    "tire_wear": (
        "타이어가 얼마나 빠르게 마모되는지를 나타냅니다. "
        "일반적으로 마모가 적을수록 장거리 레이스에서 유리합니다."
    ),
}

BASE_STATS = {stat: 55 for stat in STATS}
BASE_STATS.update(
    drag=45,
    tire_wear=45,
)


PARTS = {
    "engine": {
        "Velocity V10": {
            "top_speed": 16,
            "acceleration": 6,
            "stability": -5,
            "drag": 3,
        },
        "Pulse Hybrid": {
            "acceleration": 15,
            "top_speed": 6,
            "stability": 2,
            "tire_wear": 2,
        },
        "Endurance-X": {
            "stability": 12,
            "acceleration": 5,
            "top_speed": -4,
            "tire_wear": -4,
        },
    },
    "front_wing": {
        "Falcon High-Load": {
            "downforce": 14,
            "cornering": 10,
            "drag": 9,
            "top_speed": -4,
        },
        "Razor Low-Drag": {
            "top_speed": 9,
            "drag": -12,
            "downforce": -7,
            "cornering": -5,
        },
        "Vector Balanced": {
            "downforce": 7,
            "cornering": 6,
            "drag": 3,
            "stability": 3,
        },
    },
    "rear_wing": {
        "Monaco Blade": {
            "downforce": 14,
            "grip": 5,
            "drag": 10,
            "top_speed": -5,
        },
        "Monza Sprint": {
            "top_speed": 10,
            "drag": -11,
            "downforce": -8,
            "stability": -3,
        },
        "Apex Dualplane": {
            "downforce": 7,
            "stability": 6,
            "drag": 4,
        },
    },
    "floor": {
        "Groundforce Venturi": {
            "downforce": 15,
            "cornering": 8,
            "drag": 5,
            "stability": -2,
        },
        "Streamline Diffuser": {
            "drag": -9,
            "top_speed": 7,
            "downforce": 3,
        },
        "Stable Channel": {
            "stability": 10,
            "downforce": 7,
            "cornering": 4,
            "drag": 4,
        },
    },
    "tires": {
        "Soft": {
            "grip": 16,
            "cornering": 10,
            "acceleration": 5,
            "tire_wear": 17,
        },
        "Medium": {
            "grip": 9,
            "cornering": 6,
            "tire_wear": 7,
            "stability": 3,
        },
        "Hard": {
            "grip": 3,
            "stability": 7,
            "tire_wear": -12,
            "top_speed": 2,
        },
    },
    "suspension": {
        "Reactive Stiff": {
            "cornering": 12,
            "stability": -4,
            "grip": 5,
            "tire_wear": 6,
        },
        "Adaptive Balance": {
            "stability": 9,
            "cornering": 7,
            "tire_wear": -2,
        },
        "Compliant Enduro": {
            "stability": 12,
            "grip": 5,
            "cornering": -3,
            "tire_wear": -9,
        },
    },
    "brakes": {
        "Carbon Attack": {
            "braking": 16,
            "stability": -3,
            "tire_wear": 5,
        },
        "Progressive Control": {
            "braking": 10,
            "stability": 8,
            "cornering": 3,
        },
        "Endurance Ceramic": {
            "braking": 7,
            "stability": 5,
            "tire_wear": -7,
        },
    },
}

PART_NAMES = {
    "engine": "엔진",
    "front_wing": "프론트 윙",
    "rear_wing": "리어 윙",
    "floor": "플로어 / 디퓨저",
    "tires": "타이어",
    "suspension": "서스펜션",
    "brakes": "브레이크",
}


TEAM_PROFILES = {
    "크림슨 에이펙스": {
        "top_speed": 82,
        "downforce": 76,
        "grip": 72,
        "stability": 68,
        "cornering": 78,
        "tire_wear": 55,
    },
    "실버 벡터": {
        "top_speed": 74,
        "downforce": 80,
        "grip": 78,
        "stability": 86,
        "cornering": 82,
        "tire_wear": 38,
    },
    "옵시디언 벨로시티": {
        "top_speed": 91,
        "downforce": 62,
        "grip": 66,
        "stability": 70,
        "cornering": 64,
        "tire_wear": 50,
    },
    "에메랄드 인듀어런스": {
        "top_speed": 70,
        "downforce": 72,
        "grip": 75,
        "stability": 90,
        "cornering": 74,
        "tire_wear": 28,
    },
}


# =========================================================
# 전체 디자인
# =========================================================

CSS = """
<style>
@import url(
    'https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Rajdhani:wght@500;700&display=swap'
);

.stApp {
    background:
        radial-gradient(circle at 70% 0, #27070d, #08090c 42%, #030405);
    color: #f5f6f7;
}

.block-container {
    max-width: 1550px;
    padding: 1rem 2rem 4rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    font-family: "Black Han Sans", sans-serif;
}

.stButton button {
    min-height: 46px;
    border: 0 !important;
    border-radius: 2px !important;
    background: #e10600 !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    transition: 0.2s ease;
}

.stButton button:hover {
    filter: brightness(1.2);
    transform: translateY(-1px);
}

.hero {
    display: flex;
    min-height: 250px;
    flex-direction: column;
    justify-content: center;
    padding: 42px;
    border-bottom: 5px solid #e10600;
    background:
        linear-gradient(90deg, #08090cf2, #08090c55),
        repeating-linear-gradient(
            135deg,
            #191b20 0,
            #191b20 2px,
            #0a0b0e 2px,
            #0a0b0e 16px
        );
}

.hero h1 {
    margin: 0;
    font-size: 64px;
}

.hero p {
    color: #c4c7cc;
    font-size: 20px;
}

.panel {
    margin: 8px 0;
    padding: 18px;
    border: 1px solid #292c34;
    border-left: 3px solid #e10600;
    background: #101217;
}

.eyebrow {
    color: #e10600;
    font-family: Rajdhani, sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
}

.metric-title {
    border-bottom: 1px dotted #aaaaaa;
    cursor: help;
    font-family: Rajdhani, sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
}

.performance-bar {
    height: 8px;
    margin: 5px 0 13px;
    overflow: hidden;
    background: #252831;
    transform: skew(-10deg);
}

.performance-fill {
    height: 100%;
    background: linear-gradient(90deg, #e10600, #ffba08);
}

.big-menu {
    min-height: 120px;
    padding: 22px;
    border-top: 4px solid #e10600;
    background: #111319;
}

.tip-card {
    height: 100%;
    padding: 16px;
    border: 1px solid #2a2d35;
    background: #111319;
}

.tip-card b {
    color: #ff3430;
}

.tag {
    padding: 3px 8px;
    border: 1px solid #e1060066;
    background: #e1060028;
    color: #ff706c;
}

.muted {
    color: #9ea2aa;
}

.car-frame {
    padding: 4px;
    border: 1px solid #2b2f38;
    background:
        radial-gradient(ellipse at center, #252b36, #07080a 70%);
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# =========================================================
# 세션 초기화
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "홈"

if "parts" not in st.session_state:
    st.session_state.parts = {
        category: list(options)[0]
        for category, options in PARTS.items()
    }

if "color" not in st.session_state:
    st.session_state.color = "#E10600"

if "race_on" not in st.session_state:
    st.session_state.race_on = False


# =========================================================
# 공통 함수
# =========================================================

def calculate_stats():
    """현재 장착된 파츠를 기준으로 차량 성능을 계산한다."""

    result = BASE_STATS.copy()

    for category, selected_part in st.session_state.parts.items():
        modifiers = PARTS[category][selected_part]

        for stat, amount in modifiers.items():
            result[stat] += amount

    return {
        stat: max(10, min(99, round(value)))
        for stat, value in result.items()
    }


def change_page(page):
    st.session_state.page = page
    st.rerun()


def navigation():
    columns = st.columns([1.5, 1, 1, 1, 1, 1, 1])

    columns[0].markdown("## 🏎️ MY F1 GARAGE")

    menu = [
        "홈",
        "차고",
        "공력 테스트",
        "레이스",
        "팀 매칭",
        "성향 테스트",
    ]

    for column, page in zip(columns[1:], menu):
        if column.button(page, use_container_width=True):
            change_page(page)


def performance_gauges(current_stats):
    """성능 막대 및 한국어 Tooltip을 표시한다."""

    for stat in STATS:
        value = current_stats[stat]

        if stat in ("drag", "tire_wear"):
            quality = 100 - value
        else:
            quality = value

        hue_rotation = 0 if quality > 55 else 320

        st.markdown(
            f"""
            <div title="{HELP[stat]}">
                <span class="metric-title">
                    {LABELS[stat]} ⓘ
                </span>
                <b style="float:right">
                    {value}
                </b>

                <div class="performance-bar">
                    <div
                        class="performance-fill"
                        style="
                            width:{value}%;
                            filter:hue-rotate({hue_rotation}deg);
                        "
                    ></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
# =========================================================
# Three.js 3D 차량 뷰어
# =========================================================

def render_3d_car(height=600):
    """
    Three.js로 제작한 오리지널 포뮬러 차량을 표시한다.

    조작:
    - 마우스 왼쪽 드래그: 회전
    - 마우스 휠: 확대/축소
    - 마우스 오른쪽 드래그: 화면 이동
    """

    config = {
        "color": st.session_state.color,
        "front_wing": st.session_state.parts["front_wing"],
        "rear_wing": st.session_state.parts["rear_wing"],
        "tire": st.session_state.parts["tires"],
        "floor": st.session_state.parts["floor"],
    }

    car_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">

    <style>
        * {
            box-sizing: border-box;
        }

        html,
        body {
            width: 100%;
            height: 100%;
            margin: 0;
            overflow: hidden;
            background:
                radial-gradient(
                    ellipse at center,
                    #252b35 0%,
                    #0b0d11 45%,
                    #050608 75%
                );
            color: #ffffff;
            font-family: Arial, sans-serif;
        }

        #viewer-title {
            position: absolute;
            top: 14px;
            left: 18px;
            z-index: 5;
            font-size: 16px;
            font-weight: 900;
            letter-spacing: 2px;
            pointer-events: none;
        }

        #viewer-title span {
            color: #ef241c;
        }

        #viewer-help {
            position: absolute;
            bottom: 14px;
            left: 18px;
            z-index: 5;
            padding: 8px 12px;
            border: 1px solid #ffffff22;
            background: #050608bb;
            color: #b8bdc7;
            font-size: 12px;
            pointer-events: none;
        }

        #part-info {
            position: absolute;
            top: 14px;
            right: 18px;
            z-index: 5;
            max-width: 250px;
            padding: 10px 13px;
            border-right: 3px solid #e10600;
            background: #050608cc;
            color: #d4d7dd;
            font-size: 11px;
            line-height: 1.6;
            pointer-events: none;
        }

        canvas {
            display: block;
        }
    </style>
</head>

<body>
    <div id="viewer-title">
        AF-01 <span>360° 차량 뷰어</span>
    </div>

    <div id="part-info"></div>

    <div id="viewer-help">
        마우스 드래그: 회전 · 휠: 확대/축소 · 우클릭 드래그: 이동
    </div>

    <script type="importmap">
    {
        "imports": {
            "three":
                "https://unpkg.com/three@0.160.0/build/three.module.js",
            "three/addons/":
                "https://unpkg.com/three@0.160.0/examples/jsm/"
        }
    }
    </script>

    <script type="module">
        import * as THREE from "three";

        import {
            OrbitControls
        } from "three/addons/controls/OrbitControls.js";


        const CONFIG = __CAR_CONFIG__;


        // -------------------------------------------------
        // 기본 장면
        // -------------------------------------------------

        const scene = new THREE.Scene();

        scene.fog = new THREE.Fog(
            0x050608,
            14,
            27
        );


        const camera = new THREE.PerspectiveCamera(
            42,
            window.innerWidth / window.innerHeight,
            0.1,
            100
        );

        camera.position.set(
            8.5,
            5.2,
            10.5
        );


        const renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true
        });

        renderer.setPixelRatio(
            Math.min(window.devicePixelRatio, 2)
        );

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );

        renderer.shadowMap.enabled = true;

        renderer.shadowMap.type =
            THREE.PCFSoftShadowMap;

        renderer.outputColorSpace =
            THREE.SRGBColorSpace;

        document.body.appendChild(
            renderer.domElement
        );


        // -------------------------------------------------
        // 카메라 회전 컨트롤
        // -------------------------------------------------

        const controls = new OrbitControls(
            camera,
            renderer.domElement
        );

        controls.enableDamping = true;

        controls.dampingFactor = 0.07;

        controls.target.set(
            0,
            0.72,
            0
        );

        controls.minDistance = 5;

        controls.maxDistance = 18;

        controls.maxPolarAngle =
            Math.PI * 0.95;

        controls.minPolarAngle =
            Math.PI * 0.03;


        // -------------------------------------------------
        // 재질
        // -------------------------------------------------

        const bodyMaterial =
            new THREE.MeshStandardMaterial({
                color: CONFIG.color,
                metalness: 0.68,
                roughness: 0.24
            });


        const darkMaterial =
            new THREE.MeshStandardMaterial({
                color: 0x08090b,
                metalness: 0.5,
                roughness: 0.35
            });


        const carbonMaterial =
            new THREE.MeshStandardMaterial({
                color: 0x16181b,
                metalness: 0.25,
                roughness: 0.62
            });


        const tireMaterial =
            new THREE.MeshStandardMaterial({
                color: 0x080808,
                roughness: 0.9
            });


        const rimMaterial =
            new THREE.MeshStandardMaterial({
                color: 0xbfc5cb,
                metalness: 0.9,
                roughness: 0.18
            });


        const glassMaterial =
            new THREE.MeshStandardMaterial({
                color: 0x68b7d2,
                metalness: 0.15,
                roughness: 0.16,
                transparent: true,
                opacity: 0.75
            });


        const redTireMaterial =
            new THREE.MeshStandardMaterial({
                color: 0xe10600,
                roughness: 0.72
            });


        const yellowTireMaterial =
            new THREE.MeshStandardMaterial({
                color: 0xffd500,
                roughness: 0.72
            });


        const whiteTireMaterial =
            new THREE.MeshStandardMaterial({
                color: 0xf5f5f5,
                roughness: 0.72
            });


        // -------------------------------------------------
        // 편의 함수
        // -------------------------------------------------

        function createBox(
            width,
            height,
            depth,
            x,
            y,
            z,
            material = bodyMaterial
        ) {
            const geometry =
                new THREE.BoxGeometry(
                    width,
                    height,
                    depth
                );

            const mesh =
                new THREE.Mesh(
                    geometry,
                    material
                );

            mesh.position.set(
                x,
                y,
                z
            );

            mesh.castShadow = true;

            mesh.receiveShadow = true;

            scene.add(mesh);

            return mesh;
        }


        function createExtrudedShape(
            points,
            depth,
            material = bodyMaterial
        ) {
            const shape =
                new THREE.Shape();

            points.forEach(
                (point, index) => {
                    if (index === 0) {
                        shape.moveTo(
                            point[0],
                            point[1]
                        );
                    } else {
                        shape.lineTo(
                            point[0],
                            point[1]
                        );
                    }
                }
            );

            shape.closePath();

            const geometry =
                new THREE.ExtrudeGeometry(
                    shape,
                    {
                        depth: depth,
                        bevelEnabled: true,
                        bevelSize: 0.08,
                        bevelThickness: 0.08,
                        bevelSegments: 3
                    }
                );

            const mesh =
                new THREE.Mesh(
                    geometry,
                    material
                );

            mesh.rotation.x =
                Math.PI / 2;

            mesh.position.z =
                -depth / 2;

            mesh.castShadow = true;

            mesh.receiveShadow = true;

            scene.add(mesh);

            return mesh;
        }


        function createWheel(
            x,
            z,
            radius,
            width,
            stripeMaterial
        ) {
            const tireGeometry =
                new THREE.CylinderGeometry(
                    radius,
                    radius,
                    width,
                    36
                );

            const tire =
                new THREE.Mesh(
                    tireGeometry,
                    tireMaterial
                );

            tire.rotation.x =
                Math.PI / 2;

            tire.position.set(
                x,
                radius,
                z
            );

            tire.castShadow = true;

            scene.add(tire);


            const rimGeometry =
                new THREE.CylinderGeometry(
                    radius * 0.55,
                    radius * 0.55,
                    width + 0.025,
                    26
                );

            const rim =
                new THREE.Mesh(
                    rimGeometry,
                    rimMaterial
                );

            rim.rotation.x =
                Math.PI / 2;

            rim.position.copy(
                tire.position
            );

            scene.add(rim);


            const stripeGeometry =
                new THREE.TorusGeometry(
                    radius * 0.84,
                    0.025,
                    8,
                    40
                );

            const outsideStripe =
                new THREE.Mesh(
                    stripeGeometry,
                    stripeMaterial
                );

            outsideStripe.rotation.x =
                Math.PI / 2;

            outsideStripe.position.set(
                x,
                radius,
                z + width / 2 + 0.018
            );

            scene.add(outsideStripe);


            const insideStripe =
                outsideStripe.clone();

            insideStripe.position.z =
                z - width / 2 - 0.018;

            scene.add(insideStripe);
        }


        // -------------------------------------------------
        // 플로어
        // -------------------------------------------------

        const floorWidth =
            CONFIG.floor.includes("Groundforce")
                ? 1.92
                : CONFIG.floor.includes("Streamline")
                ? 1.62
                : 1.78;


        createBox(
            6.8,
            0.10,
            floorWidth,
            0,
            0.14,
            0,
            carbonMaterial
        );


        // 바지보드 / 플로어 가장자리

        createBox(
            2.8,
            0.09,
            0.14,
            0.25,
            0.26,
            floorWidth / 2,
            carbonMaterial
        );

        createBox(
            2.8,
            0.09,
            0.14,
            0.25,
            0.26,
            -floorWidth / 2,
            carbonMaterial
        );


        // -------------------------------------------------
        // 메인 차체 실루엣
        // -------------------------------------------------

        createExtrudedShape(
            [
                [-3.95, 0.28],
                [-3.58, 0.18],
                [-2.55, 0.12],
                [-1.65, 0.16],
                [-0.92, 0.29],
                [-0.2, 0.43],
                [1.25, 0.58],
                [2.62, 0.56],
                [3.28, 0.42],
                [3.62, 0.24],
                [2.70, 0.11],
                [-3.1, 0.09]
            ],
            1.10,
            bodyMaterial
        );


        // 노즈 상단

        createExtrudedShape(
            [
                [-3.75, 0.42],
                [-3.22, 0.34],
                [-2.45, 0.37],
                [-1.58, 0.51],
                [-1.15, 0.69],
                [-2.22, 0.66],
                [-3.18, 0.53]
            ],
            0.48,
            bodyMaterial
        );


        // -------------------------------------------------
        // 사이드포드
        // -------------------------------------------------

        const leftSidepod =
            createExtrudedShape(
                [
                    [-0.95, 0.34],
                    [-0.35, 0.47],
                    [0.28, 0.92],
                    [1.55, 1.02],
                    [2.32, 0.64],
                    [1.74, 0.30]
                ],
                0.48,
                bodyMaterial
            );

        leftSidepod.position.z =
            0.38;


        const rightSidepod =
            leftSidepod.clone();

        rightSidepod.position.z =
            -0.86;

        scene.add(rightSidepod);


        // 사이드포드 공기 흡입구

        createBox(
            0.45,
            0.35,
            0.12,
            0.24,
            0.78,
            0.67,
            darkMaterial
        );

        createBox(
            0.45,
            0.35,
            0.12,
            0.24,
            0.78,
            -0.67,
            darkMaterial
        );


        // -------------------------------------------------
        // 콕핏 및 헤드레스트
        // -------------------------------------------------

        createBox(
            1.32,
            0.24,
            0.77,
            0.72,
            0.88,
            0,
            bodyMaterial
        );


        const cockpit =
            createBox(
                0.98,
                0.22,
                0.60,
                0.28,
                1.14,
                0,
                darkMaterial
            );

        cockpit.rotation.z = -0.07;


        createBox(
            0.38,
            0.25,
            0.47,
            0.02,
            1.20,
            0,
            glassMaterial
        );


        // 에어박스

        createBox(
            0.55,
            0.72,
            0.48,
            1.12,
            1.12,
            0,
            bodyMaterial
        );

        createBox(
            0.22,
            0.28,
            0.33,
            1.04,
            1.48,
            0,
            darkMaterial
        );


        // -------------------------------------------------
        // Halo
        // -------------------------------------------------

        const haloLeft =
            createBox(
                0.085,
                0.75,
                0.085,
                0.23,
                1.48,
                0.28,
                darkMaterial
            );

        haloLeft.rotation.z = -0.28;


        const haloRight =
            createBox(
                0.085,
                0.75,
                0.085,
                0.23,
                1.48,
                -0.28,
                darkMaterial
            );

        haloRight.rotation.z = -0.28;


        createBox(
            0.085,
            0.58,
            0.085,
            0.54,
            1.56,
            0,
            darkMaterial
        );


        createBox(
            0.60,
            0.085,
            0.70,
            0.42,
            1.75,
            0,
            darkMaterial
        );


        // -------------------------------------------------
        // 프론트 윙
        // -------------------------------------------------

        let frontWingWidth = 2.5;
        let frontWingLayers = 2;

        if (
            CONFIG.front_wing.includes(
                "High-Load"
            )
        ) {
            frontWingWidth = 3.05;
            frontWingLayers = 4;
        } else if (
            CONFIG.front_wing.includes(
                "Low-Drag"
            )
        ) {
            frontWingWidth = 2.15;
            frontWingLayers = 1;
        }


        createBox(
            0.18,
            0.07,
            frontWingWidth,
            -3.75,
            0.26,
            0,
            carbonMaterial
        );


        for (
            let layer = 0;
            layer < frontWingLayers;
            layer++
        ) {
            const wingElement =
                createBox(
                    0.48 - layer * 0.045,
                    0.05,
                    frontWingWidth * (
                        0.94 - layer * 0.035
                    ),
                    -3.54 + layer * 0.16,
                    0.39 + layer * 0.105,
                    0,
                    layer % 2 === 0
                        ? bodyMaterial
                        : carbonMaterial
                );

            wingElement.rotation.z =
                -0.03 * layer;
        }


        createBox(
            0.10,
            0.56,
            0.08,
            -3.60,
            0.46,
            frontWingWidth / 2,
            carbonMaterial
        );

        createBox(
            0.10,
            0.56,
            0.08,
            -3.60,
            0.46,
            -frontWingWidth / 2,
            carbonMaterial
        );


        // -------------------------------------------------
        // 리어 윙
        // -------------------------------------------------

        let rearWingHeight = 1.25;
        let rearWingWidth = 2.05;
        let rearWingLayers = 1;

        if (
            CONFIG.rear_wing.includes(
                "Monaco"
            )
        ) {
            rearWingHeight = 1.64;
            rearWingWidth = 2.4;
            rearWingLayers = 2;
        } else if (
            CONFIG.rear_wing.includes(
                "Monza"
            )
        ) {
            rearWingHeight = 1.03;
            rearWingWidth = 1.90;
            rearWingLayers = 1;
        }


        createBox(
            0.13,
            0.78,
            0.11,
            2.92,
            rearWingHeight - 0.37,
            rearWingWidth / 2,
            carbonMaterial
        );

        createBox(
            0.13,
            0.78,
            0.11,
            2.92,
            rearWingHeight - 0.37,
            -rearWingWidth / 2,
            carbonMaterial
        );


        for (
            let layer = 0;
            layer < rearWingLayers;
            layer++
        ) {
            const rearElement =
                createBox(
                    0.38,
                    0.10,
                    rearWingWidth,
                    3.05 - layer * 0.16,
                    rearWingHeight - layer * 0.25,
                    0,
                    layer === 0
                        ? bodyMaterial
                        : carbonMaterial
                );

            rearElement.rotation.z =
                CONFIG.rear_wing.includes("Monza")
                    ? -0.14
                    : -0.04;
        }


        // 빔 윙

        createBox(
            0.34,
            0.07,
            rearWingWidth * 0.78,
            2.83,
            0.62,
            0,
            carbonMaterial
        );


        // -------------------------------------------------
        // 디퓨저
        // -------------------------------------------------

        const diffuserWidth =
            CONFIG.floor.includes("Groundforce")
                ? 1.7
                : 1.42;


        const diffuser =
            createBox(
                0.82,
                0.12,
                diffuserWidth,
                3.20,
                0.24,
                0,
                carbonMaterial
            );

        diffuser.rotation.z = 0.12;


        for (
            let index = -2;
            index <= 2;
            index++
        ) {
            createBox(
                0.68,
                0.24,
                0.035,
                3.16,
                0.32,
                index * diffuserWidth / 5,
                carbonMaterial
            );
        }


        // -------------------------------------------------
        // 타이어
        // -------------------------------------------------

        let tireRadius = 0.59;
        let tireStripeMaterial =
            yellowTireMaterial;

        if (CONFIG.tire === "Soft") {
            tireRadius = 0.62;
            tireStripeMaterial =
                redTireMaterial;
        } else if (
            CONFIG.tire === "Hard"
        ) {
            tireRadius = 0.56;
            tireStripeMaterial =
                whiteTireMaterial;
        }


        // 프론트 휠

        createWheel(
            -2.28,
            1.10,
            tireRadius,
            0.36,
            tireStripeMaterial
        );

        createWheel(
            -2.28,
            -1.10,
            tireRadius,
            0.36,
            tireStripeMaterial
        );


        // 리어 휠

        createWheel(
            2.18,
            1.11,
            tireRadius * 1.09,
            0.44,
            tireStripeMaterial
        );

        createWheel(
            2.18,
            -1.11,
            tireRadius * 1.09,
            0.44,
            tireStripeMaterial
        );


        // -------------------------------------------------
        // 서스펜션 암
        // -------------------------------------------------

        function createSuspensionArm(
            start,
            end
        ) {
            const direction =
                new THREE.Vector3()
                    .subVectors(end, start);

            const length =
                direction.length();

            const geometry =
                new THREE.CylinderGeometry(
                    0.025,
                    0.025,
                    length,
                    10
                );

            const arm =
                new THREE.Mesh(
                    geometry,
                    carbonMaterial
                );

            arm.position.copy(
                start
                    .clone()
                    .add(end)
                    .multiplyScalar(0.5)
            );

            arm.quaternion.setFromUnitVectors(
                new THREE.Vector3(0, 1, 0),
                direction
                    .clone()
                    .normalize()
            );

            scene.add(arm);
        }


        createSuspensionArm(
            new THREE.Vector3(-2.0, 0.45, 0.48),
            new THREE.Vector3(-2.28, 0.55, 1.02)
        );

        createSuspensionArm(
            new THREE.Vector3(-2.0, 0.67, 0.48),
            new THREE.Vector3(-2.28, 0.40, 1.02)
        );

        createSuspensionArm(
            new THREE.Vector3(-2.0, 0.45, -0.48),
            new THREE.Vector3(-2.28, 0.55, -1.02)
        );

        createSuspensionArm(
            new THREE.Vector3(-2.0, 0.67, -0.48),
            new THREE.Vector3(-2.28, 0.40, -1.02)
        );


        // -------------------------------------------------
        // 바닥 및 조명
        // -------------------------------------------------

        const ground =
            new THREE.Mesh(
                new THREE.PlaneGeometry(
                    40,
                    40
                ),
                new THREE.MeshStandardMaterial({
                    color: 0x101216,
                    roughness: 0.92,
                    metalness: 0.05
                })
            );

        ground.rotation.x =
            -Math.PI / 2;

        ground.receiveShadow = true;

        scene.add(ground);


        const grid =
            new THREE.GridHelper(
                30,
                30,
                0x4a4d55,
                0x24262c
            );

        grid.position.y = 0.005;

        scene.add(grid);


        const hemisphereLight =
            new THREE.HemisphereLight(
                0xffffff,
                0x141525,
                2.1
            );

        scene.add(
            hemisphereLight
        );


        const mainLight =
            new THREE.DirectionalLight(
                0xffffff,
                5.2
            );

        mainLight.position.set(
            -4,
            8,
            5
        );

        mainLight.castShadow = true;

        scene.add(
            mainLight
        );


        const redLight =
            new THREE.PointLight(
                0xff160d,
                34,
                16
            );

        redLight.position.set(
            -4,
            2.5,
            -3
        );

        scene.add(
            redLight
        );


        const blueLight =
            new THREE.PointLight(
                0x159dff,
                18,
                14
            );

        blueLight.position.set(
            4,
            3,
            4
        );

        scene.add(
            blueLight
        );


        // -------------------------------------------------
        // 화면 설명
        // -------------------------------------------------

        document.getElementById(
            "part-info"
        ).innerHTML = `
            프론트 윙: ${CONFIG.front_wing}<br>
            리어 윙: ${CONFIG.rear_wing}<br>
            타이어: ${CONFIG.tire}<br>
            플로어: ${CONFIG.floor}
        `;


        // -------------------------------------------------
        // 애니메이션
        // -------------------------------------------------

        function animate() {
            requestAnimationFrame(
                animate
            );

            controls.update();

            renderer.render(
                scene,
                camera
            );
        }

        animate();


        window.addEventListener(
            "resize",
            () => {
                camera.aspect =
                    window.innerWidth /
                    window.innerHeight;

                camera.updateProjectionMatrix();

                renderer.setSize(
                    window.innerWidth,
                    window.innerHeight
                );
            }
        );
    </script>
</body>
</html>
"""

    car_html = car_html.replace(
        "__CAR_CONFIG__",
        json.dumps(config),
    )

    components.html(
        car_html,
        height=height,
        scrolling=False,
    )


# =========================================================
# 홈
# =========================================================

def render_home():
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">
                나만의 포뮬러 레이싱 경험
            </div>

            <h1>MY F1 GARAGE</h1>

            <p>
                차량을 설계하고, 공기역학을 시험하고,
                트랙에서 직접 달려보세요.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    render_3d_car(height=410)

    menu_items = [
        (
            "차량 만들기",
            "파츠를 고르고 3D 차량을 직접 조립합니다.",
            "차고",
        ),
        (
            "레이스",
            "WASD 키로 AI 차량과 직접 경쟁합니다.",
            "레이스",
        ),
        (
            "공력 테스트",
            "다운포스와 공기저항을 분석합니다.",
            "공력 테스트",
        ),
        (
            "팀 매칭",
            "차량의 설계 철학과 가까운 팀을 찾습니다.",
            "팀 매칭",
        ),
        (
            "레이싱 성향 테스트",
            "나의 드라이버 성향을 확인합니다.",
            "성향 테스트",
        ),
        (
            "튜토리얼",
            "게임 조작과 차량 성능을 배웁니다.",
            "튜토리얼",
        ),
    ]

    columns = st.columns(3)

    for index, (
        title,
        description,
        target_page,
    ) in enumerate(menu_items):
        with columns[index % 3]:
            st.markdown(
                f"""
                <div class="big-menu">
                    <h3>{title}</h3>

                    <p class="muted">
                        {description}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                f"{title} 시작",
                key=f"home_{target_page}",
                use_container_width=True,
            ):
                change_page(target_page)


# =========================================================
# 차고
# =========================================================

def render_garage():
    st.title("차고 · 나만의 차량 제작")

    st.caption(
        "왼쪽에서 파츠를 선택하고, 가운데의 3D 차량을 회전해 "
        "외형을 확인한 뒤 오른쪽에서 차량 성능을 확인하세요."
    )

    left_column, center_column, right_column = st.columns(
        [0.85, 1.6, 0.85]
    )

    with left_column:
        st.subheader("파츠 선택")

        for category, options in PARTS.items():
            current_part = (
                st.session_state.parts[category]
            )

            option_names = list(options)

            selected_part = st.selectbox(
                PART_NAMES[category],
                option_names,
                index=option_names.index(
                    current_part
                ),
                key=f"part_{category}",
            )

            st.session_state.parts[
                category
            ] = selected_part

            modifiers = options[
                selected_part
            ]

            modifier_text = " · ".join(
                f"{LABELS[stat]} {amount:+}"
                for stat, amount
                in modifiers.items()
            )

            st.caption(
                modifier_text
            )

        st.session_state.color = (
            st.color_picker(
                "차체 색상",
                st.session_state.color,
            )
        )

    with center_column:
        st.markdown(
            '<div class="car-frame">',
            unsafe_allow_html=True,
        )

        render_3d_car(
            height=620
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with right_column:
        st.subheader("차량 성능")

        current_stats = (
            calculate_stats()
        )

        performance_gauges(
            current_stats
        )

        st.info(
            "ⓘ 표시 또는 성능 지표 위에 마우스를 올리면 "
            "한국어 설명을 볼 수 있습니다.\n\n"
            "DRAG와 TIRE WEAR는 낮을수록 유리합니다."
        )

        if st.button(
            "설계 확정 → 공력 테스트",
            use_container_width=True,
        ):
            change_page(
                "공력 테스트"
            )


# =========================================================
# 튜토리얼
# =========================================================

def render_tutorial():
    st.title("튜토리얼 · 처음부터 레이스까지")

    tutorial_steps = [
        (
            "STEP 1",
            "차량 제작",
            "차고에서 엔진, 윙, 타이어, 플로어, "
            "서스펜션과 브레이크를 선택합니다.",
        ),
        (
            "STEP 2",
            "차량 성능 확인",
            "파츠를 변경하며 각 선택이 성능에 미치는 "
            "장점과 단점을 확인합니다.",
        ),
        (
            "STEP 3",
            "3D 차량 검사",
            "마우스로 차량을 회전하고 확대하면서 "
            "선택한 윙과 타이어가 반영됐는지 확인합니다.",
        ),
        (
            "STEP 4",
            "공력 테스트",
            "DOWNFORCE와 DRAG, 예상 랩타임을 확인하고 "
            "필요하면 다시 차고로 돌아가 세팅을 변경합니다.",
        ),
        (
            "STEP 5",
            "직접 레이스",
            "WASD로 차량을 운전하고 ERS와 DRS를 활용해 "
            "AI 차량을 추월합니다.",
        ),
        (
            "STEP 6",
            "설계 성향 분석",
            "완주 후 차량 설계 성향과 가장 가까운 "
            "게임 속 가상 팀을 확인합니다.",
        ),
    ]

    for step, title, description in tutorial_steps:
        st.markdown(
            f"""
            <div class="panel">
                <div class="eyebrow">
                    {step}
                </div>

                <h3>{title}</h3>

                <p class="muted">
                    {description}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader(
        "기본 조작"
    )

    control_columns = st.columns(4)

    control_data = [
        (
            "W / S",
            "가속 / 브레이크",
        ),
        (
            "A / D",
            "좌우 조향",
        ),
        (
            "SHIFT",
            "ERS 사용",
        ),
        (
            "E",
            "DRS 사용",
        ),
        (
            "Q / Z",
            "수동 업시프트 / 다운시프트",
        ),
        (
            "R",
            "레이스 재시작",
        ),
        (
            "마우스 드래그",
            "3D 차량 회전",
        ),
        (
            "마우스 휠",
            "3D 차량 확대 / 축소",
        ),
    ]

    for index, (
        key_name,
        description,
    ) in enumerate(control_data):
        with control_columns[index % 4]:
            st.markdown(
                f"""
                <div class="tip-card">
                    <b>{key_name}</b>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader(
        "차량 성능 이해하기"
    )

    high_explanations = {
        "top_speed":
            "긴 직선에서 최고속도가 높아져 추월과 방어에 유리합니다.",
        "acceleration":
            "출발과 코너 탈출 시 빠르게 속도를 올릴 수 있습니다.",
        "downforce":
            "고속 코너에서 차량이 안정적이지만 DRAG가 늘 수 있습니다.",
        "grip":
            "제동과 저속 코너에서 타이어가 노면을 더 잘 붙잡습니다.",
        "stability":
            "급격한 조향과 제동에서도 차량의 움직임이 안정적입니다.",
        "braking":
            "코너에 더 늦게 진입해도 빠르고 안정적으로 감속합니다.",
        "cornering":
            "코너를 더 빠른 속도로 통과할 수 있습니다.",
        "drag":
            "공기저항이 커져 직선 최고속도와 가속에 불리합니다.",
        "tire_wear":
            "타이어가 빠르게 닳아 장거리 레이스에서 불리합니다.",
    }

    low_explanations = {
        "top_speed":
            "직선에서 추월하거나 상대를 방어하기 어려워집니다.",
        "acceleration":
            "코너 탈출과 출발에서 속도를 올리는 데 시간이 걸립니다.",
        "downforce":
            "직선 효율은 좋아질 수 있지만 고속 코너가 불안정합니다.",
        "grip":
            "미끄러짐이 커지고 제동거리가 길어질 수 있습니다.",
        "stability":
            "급격한 조작에서 차량의 뒤가 쉽게 미끄러질 수 있습니다.",
        "braking":
            "코너 진입 전에 더 일찍 제동해야 합니다.",
        "cornering":
            "코너 진입 속도를 더 많이 줄여야 합니다.",
        "drag":
            "직선 효율은 좋아지지만 다운포스 부족에 주의해야 합니다.",
        "tire_wear":
            "타이어 성능을 오래 유지해 장거리 레이스에 유리합니다.",
    }

    stat_columns = st.columns(3)

    for index, stat in enumerate(STATS):
        with stat_columns[index % 3]:
            st.markdown(
                f"""
                <div class="tip-card">
                    <b>{LABELS[stat]}</b>

                    <p>
                        {HELP[stat]}
                    </p>

                    <small>
                        <strong>수치가 높을 때</strong><br>
                        {high_explanations[stat]}
                        <br><br>

                        <strong>수치가 낮을 때</strong><br>
                        {low_explanations[stat]}
                    </small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if st.button(
        "차량 제작 시작",
        use_container_width=True,
    ):
        change_page(
            "차고"
        )


# =========================================================
# 공력 테스트
# =========================================================

def calculate_expected_lap_time(
    current_stats,
):
    """
    직선, 고속 코너, 저속 코너, 안정성 및 타이어 성능을
    반영해 가상의 예상 랩타임을 계산한다.
    """

    performance_score = (
        0.34
        * current_stats["top_speed"]
        + 0.18
        * current_stats["acceleration"]
        + 0.24
        * current_stats["downforce"]
        + 0.22
        * current_stats["cornering"]
        + 0.18
        * current_stats["grip"]
        + 0.14
        * current_stats["braking"]
        + 0.12
        * current_stats["stability"]
        - 0.12
        * current_stats["drag"]
        - 0.08
        * current_stats["tire_wear"]
    )

    return (
        102
        - performance_score
        * 0.19
    )


def render_aero_test():
    current_stats = (
        calculate_stats()
    )

    st.title(
        "공력 테스트 · CFD LAB"
    )

    st.caption(
        "가상 풍동에서 차량 주변의 공기 흐름, 다운포스, "
        "공기저항과 예상 랩타임을 확인합니다."
    )

    viewer_column, data_column = st.columns(
        [1.4, 0.8]
    )

    with viewer_column:
        render_3d_car(
            height=480
        )

        flow_separation = max(
            3,
            round(
                (
                    current_stats["drag"]
                    - current_stats["stability"] / 3
                )
                / 2
            ),
        )

        front_distribution = round(
            current_stats["downforce"]
            * 0.47
        )

        rear_distribution = round(
            current_stats["downforce"]
            * 0.53
        )

        st.markdown(
            f"""
            <div class="panel">
                <div class="eyebrow">
                    가상 풍동 분석
                </div>

                <h3>
                    공기 흐름 → 프론트 윙 → 플로어 →
                    디퓨저 → 리어 윙
                </h3>

                <p>
                    다운포스 계수 CL
                    <b>
                        {current_stats["downforce"] / 50:.2f}
                    </b>
                    &nbsp;&nbsp;

                    항력 계수 CD
                    <b>
                        {current_stats["drag"] / 100:.2f}
                    </b>
                </p>

                <p>
                    전후 압력 분포:
                    프론트
                    <b>{front_distribution}%</b>
                    /
                    리어
                    <b>{rear_distribution}%</b>
                </p>

                <p>
                    흐름 박리 위험:
                    <b>{flow_separation}%</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with data_column:
        st.subheader(
            "공력 성능"
        )

        performance_gauges(
            current_stats
        )

        expected_lap = (
            calculate_expected_lap_time(
                current_stats
            )
        )

        estimated_top_speed = (
            220
            + current_stats["top_speed"]
            * 1.05
            - current_stats["drag"]
            * 0.18
        )

        st.metric(
            "예상 랩타임",
            f"{expected_lap:.3f}초",
        )

        st.metric(
            "예상 최고속도",
            f"{estimated_top_speed:.0f} km/h",
        )

        if (
            current_stats["downforce"]
            >= 75
        ):
            st.success(
                "고다운포스 성향입니다. "
                "고속 코너와 테크니컬 서킷에서 유리합니다."
            )
        elif (
            current_stats["drag"]
            <= 38
        ):
            st.success(
                "저항이 낮은 직선형 세팅입니다. "
                "긴 직선과 DRS 구간에서 유리합니다."
            )
        else:
            st.info(
                "직선과 코너 성능이 균형 잡힌 세팅입니다."
            )

        if st.button(
            "이 세팅으로 레이스 준비",
            use_container_width=True,
        ):
            change_page(
                "레이스"
            )
# =========================================================
# 실시간 Canvas 레이스
# =========================================================

def build_race_html(track, total_laps, manual_gear):
    current_stats = calculate_stats()

    config = {
        "stats": current_stats,
        "color": st.session_state.color,
        "tire": st.session_state.parts["tires"],
        "track": track,
        "laps": total_laps,
        "manual": manual_gear,
    }

    race_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">

    <style>
        * {
            box-sizing: border-box;
        }

        html,
        body {
            width: 100%;
            height: 100%;
            margin: 0;
            overflow: hidden;
            background: #050608;
            color: #ffffff;
            font-family: Arial, sans-serif;
            user-select: none;
        }

        canvas {
            display: block;
            background: #101317;
        }

        #hud {
            position: absolute;
            inset: 0;
            pointer-events: none;
        }

        .top-hud {
            display: flex;
            justify-content: space-between;
            padding: 14px 20px;
            background:
                linear-gradient(
                    180deg,
                    #000000dd,
                    transparent
                );
            font-size: 22px;
            font-weight: 900;
            text-shadow: 0 2px 5px #000000;
        }

        #race-message {
            position: absolute;
            top: 72px;
            left: 50%;
            padding: 7px 16px;
            transform: translateX(-50%);
            background: #050608cc;
            color: #ffe500;
            font-size: 17px;
            font-weight: 900;
        }

        #countdown {
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-size: 100px;
            font-weight: 900;
            text-shadow:
                0 5px 20px #000000,
                0 0 30px #e10600;
        }

        .control-help {
            position: absolute;
            bottom: 105px;
            left: 15px;
            padding: 9px 12px;
            border-left: 3px solid #e10600;
            background: #000000cc;
            color: #cccccc;
            font-size: 12px;
        }

        .bottom-hud {
            position: absolute;
            right: 2%;
            bottom: 12px;
            left: 2%;
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 5px;
            padding: 10px;
            border-top: 3px solid #e10600;
            background: #050608e8;
        }

        .hud-cell {
            padding: 0 8px;
            border-right: 1px solid #34363d;
            color: #aaaaaa;
            font-size: 11px;
            text-align: center;
        }

        .hud-cell:last-child {
            border-right: 0;
        }

        .hud-cell b {
            display: block;
            color: #ffffff;
            font-size: 20px;
        }

        .hud-bar {
            height: 6px;
            margin-top: 5px;
            overflow: hidden;
            background: #292c34;
        }

        .hud-fill {
            width: 100%;
            height: 100%;
            background: #e10600;
        }

        #finish-panel {
            position: absolute;
            inset: 7% 15%;
            overflow-y: auto;
            padding: 25px;
            border: 2px solid #e10600;
            background: #090b0ff5;
            text-align: center;
            pointer-events: auto;
        }

        #finish-panel h1 {
            margin: 4px;
            color: #ffffff;
            font-size: 58px;
        }

        #finish-panel button {
            padding: 13px 32px;
            border: 0;
            background: #e10600;
            color: #ffffff;
            font-weight: 900;
            cursor: pointer;
        }

        .hidden {
            display: none;
        }
    </style>
</head>

<body tabindex="0">
    <canvas id="game"></canvas>

    <div id="hud">
        <div class="top-hud">
            <div id="lap-display">LAP 1 / 5</div>
            <div id="position-display">POSITION P1</div>
            <div id="time-display">00:00.000</div>
        </div>

        <div id="race-message"></div>
        <div id="countdown">5</div>

        <div class="control-help">
            W 가속 · S 브레이크/후진 · A/D 조향 ·
            SHIFT ERS · E DRS · Q/Z 변속 · R 재시작
        </div>

        <div class="bottom-hud">
            <div class="hud-cell">
                SPEED
                <b id="speed-display">0</b>
                km/h
            </div>

            <div class="hud-cell">
                RPM
                <b id="rpm-display">0</b>
                <div class="hud-bar">
                    <div
                        id="rpm-bar"
                        class="hud-fill"
                    ></div>
                </div>
            </div>

            <div class="hud-cell">
                GEAR
                <b id="gear-display">N</b>
            </div>

            <div class="hud-cell">
                ERS
                <b id="ers-display">100%</b>
                <div class="hud-bar">
                    <div
                        id="ers-bar"
                        class="hud-fill"
                    ></div>
                </div>
            </div>

            <div class="hud-cell">
                DRS
                <b id="drs-display">LOCKED</b>
            </div>

            <div class="hud-cell">
                TYRE
                <b id="tyre-display">100%</b>
                <div class="hud-bar">
                    <div
                        id="tyre-bar"
                        class="hud-fill"
                    ></div>
                </div>
            </div>

            <div class="hud-cell">
                FUEL
                <b id="fuel-display">100%</b>
                <div class="hud-bar">
                    <div
                        id="fuel-bar"
                        class="hud-fill"
                    ></div>
                </div>
            </div>
        </div>
    </div>

    <div
        id="finish-panel"
        class="hidden"
    ></div>

    <script>
        const CONFIG = __RACE_CONFIG__;

        const canvas =
            document.getElementById("game");

        const context =
            canvas.getContext("2d");

        const lapDisplay =
            document.getElementById("lap-display");

        const positionDisplay =
            document.getElementById("position-display");

        const timeDisplay =
            document.getElementById("time-display");

        const raceMessage =
            document.getElementById("race-message");

        const countdown =
            document.getElementById("countdown");

        const speedDisplay =
            document.getElementById("speed-display");

        const rpmDisplay =
            document.getElementById("rpm-display");

        const rpmBar =
            document.getElementById("rpm-bar");

        const gearDisplay =
            document.getElementById("gear-display");

        const ersDisplay =
            document.getElementById("ers-display");

        const ersBar =
            document.getElementById("ers-bar");

        const drsDisplay =
            document.getElementById("drs-display");

        const tyreDisplay =
            document.getElementById("tyre-display");

        const tyreBar =
            document.getElementById("tyre-bar");

        const fuelDisplay =
            document.getElementById("fuel-display");

        const fuelBar =
            document.getElementById("fuel-bar");

        const finishPanel =
            document.getElementById("finish-panel");


        let width = 0;
        let height = 0;
        let scale = 1;
        let trackPoints = [];


        const trackLayouts = {
            "고속 서킷": [
                [0.15, 0.55],
                [0.20, 0.25],
                [0.55, 0.17],
                [0.82, 0.25],
                [0.88, 0.48],
                [0.72, 0.58],
                [0.83, 0.78],
                [0.50, 0.82],
                [0.22, 0.72]
            ],

            "테크니컬 서킷": [
                [0.15, 0.35],
                [0.31, 0.18],
                [0.52, 0.29],
                [0.72, 0.17],
                [0.88, 0.35],
                [0.67, 0.47],
                [0.86, 0.68],
                [0.60, 0.82],
                [0.39, 0.68],
                [0.18, 0.80],
                [0.28, 0.53]
            ],

            "밸런스 서킷": [
                [0.13, 0.50],
                [0.22, 0.22],
                [0.55, 0.16],
                [0.83, 0.30],
                [0.78, 0.54],
                [0.90, 0.72],
                [0.58, 0.82],
                [0.35, 0.68],
                [0.16, 0.78]
            ]
        };


        function resizeCanvas() {
            width = canvas.width =
                window.innerWidth;

            height = canvas.height =
                window.innerHeight;

            scale = Math.min(
                width / 1200,
                height / 760
            );

            trackPoints =
                trackLayouts[CONFIG.track].map(
                    point => ({
                        x: point[0] * width,
                        y: point[1] * height
                    })
                );
        }

        resizeCanvas();

        window.addEventListener(
            "resize",
            resizeCanvas
        );


        // ---------------------------------------------
        // 키보드 입력
        // ---------------------------------------------

        const keys = {};

        window.addEventListener(
            "keydown",
            event => {
                keys[
                    event.key.toLowerCase()
                ] = true;

                if (
                    [
                        "w",
                        "a",
                        "s",
                        "d",
                        "e",
                        "q",
                        "z",
                        "shift"
                    ].includes(
                        event.key.toLowerCase()
                    )
                ) {
                    event.preventDefault();
                }
            }
        );

        window.addEventListener(
            "keyup",
            event => {
                keys[
                    event.key.toLowerCase()
                ] = false;
            }
        );

        document.body.focus();


        // ---------------------------------------------
        // 트랙 위 위치 계산
        // ---------------------------------------------

        function linearInterpolate(
            first,
            second,
            ratio
        ) {
            return (
                first
                + (
                    second
                    - first
                )
                * ratio
            );
        }


        function getTrackPosition(
            progress
        ) {
            const pointCount =
                trackPoints.length;

            const wrappedProgress =
                (
                    (
                        progress % 1
                    )
                    + 1
                )
                % 1;

            const pathPosition =
                wrappedProgress
                * pointCount;

            const index =
                Math.floor(
                    pathPosition
                );

            const ratio =
                pathPosition
                - index;

            const firstPoint =
                trackPoints[index];

            const secondPoint =
                trackPoints[
                    (
                        index + 1
                    )
                    % pointCount
                ];

            return {
                x: linearInterpolate(
                    firstPoint.x,
                    secondPoint.x,
                    ratio
                ),

                y: linearInterpolate(
                    firstPoint.y,
                    secondPoint.y,
                    ratio
                ),

                angle: Math.atan2(
                    secondPoint.y
                    - firstPoint.y,

                    secondPoint.x
                    - firstPoint.x
                )
            };
        }


        // ---------------------------------------------
        // 플레이어와 AI
        // ---------------------------------------------

        const player = {
            progress: 0,
            lane: 0,
            speed: 0,
            lap: 0,
            ers: 100,
            fuel: 100,
            tyre: 100,
            gear: 1,
            topSpeed: 0,
            overtakes: 0,
            drsUses: 0,
            lastDrs: false,
            shiftUpPressed: false,
            shiftDownPressed: false
        };


        const aiProfiles = [
            {
                name: "NOVA-01",
                speed: 215,
                cornering: 0.94,
                aggression: 0.92,
                stability: 0.72,
                color: "#00d1ff"
            },
            {
                name: "VECTOR-7",
                speed: 205,
                cornering: 1.08,
                aggression: 0.64,
                stability: 0.91,
                color: "#ffd000"
            },
            {
                name: "ONYX-12",
                speed: 228,
                cornering: 0.88,
                aggression: 0.81,
                stability: 0.70,
                color: "#d342ff"
            },
            {
                name: "AEGIS-4",
                speed: 200,
                cornering: 1.01,
                aggression: 0.48,
                stability: 0.96,
                color: "#20e070"
            },
            {
                name: "PULSE-9",
                speed: 211,
                cornering: 1.00,
                aggression: 0.70,
                stability: 0.82,
                color: "#ff7b00"
            }
        ];


        const aiCars =
            aiProfiles.map(
                (profile, index) => ({
                    ...profile,
                    progress:
                        0.018
                        + index * 0.018,

                    currentSpeed:
                        40 + index * 3,

                    lane:
                        (
                            index - 2
                        )
                        * 8,

                    lap: 0
                })
            );


        let raceStartTime =
            performance.now();

        let lastFrameTime =
            performance.now();

        let lapStartTime =
            performance.now();

        let lapTimes = [];

        let raceActive = false;
        let raceFinished = false;


        // ---------------------------------------------
        // 카운트다운
        // ---------------------------------------------

        const countdownValues = [
            "5",
            "4",
            "3",
            "2",
            "1"
        ];

        countdownValues.forEach(
            (value, index) => {
                setTimeout(
                    () => {
                        countdown.textContent =
                            value;
                    },
                    index * 1000
                );
            }
        );

        setTimeout(
            () => {
                countdown.textContent =
                    "GO!";

                raceActive = true;

                raceStartTime =
                    performance.now();

                lapStartTime =
                    raceStartTime;
            },
            5000
        );

        setTimeout(
            () => {
                countdown.textContent =
                    "";
            },
            5700
        );


        // ---------------------------------------------
        // 트랙 그리기
        // ---------------------------------------------

        function drawTrack() {
            context.lineCap = "round";
            context.lineJoin = "round";


            // 잔디/런오프 배경

            context.fillStyle = "#12331e";
            context.fillRect(
                0,
                0,
                width,
                height
            );


            // 트랙 외곽

            context.beginPath();

            trackPoints.forEach(
                (point, index) => {
                    if (index === 0) {
                        context.moveTo(
                            point.x,
                            point.y
                        );
                    } else {
                        context.lineTo(
                            point.x,
                            point.y
                        );
                    }
                }
            );

            context.closePath();

            context.strokeStyle =
                "#17191d";

            context.lineWidth =
                138 * scale;

            context.stroke();


            // 연석

            context.strokeStyle =
                "#e6e6e6";

            context.lineWidth =
                123 * scale;

            context.setLineDash([
                16,
                16
            ]);

            context.stroke();

            context.setLineDash([]);


            // 아스팔트

            context.strokeStyle =
                "#41444a";

            context.lineWidth =
                112 * scale;

            context.stroke();


            // 중앙 가이드

            context.strokeStyle =
                "#777777";

            context.lineWidth = 2;

            context.setLineDash([
                18,
                18
            ]);

            context.stroke();

            context.setLineDash([]);


            // 출발선

            const start =
                trackPoints[0];

            const next =
                trackPoints[1];

            const startAngle =
                Math.atan2(
                    next.y - start.y,
                    next.x - start.x
                );

            const normalX =
                Math.sin(startAngle)
                * 56
                * scale;

            const normalY =
                -Math.cos(startAngle)
                * 56
                * scale;

            context.beginPath();

            context.moveTo(
                start.x - normalX,
                start.y - normalY
            );

            context.lineTo(
                start.x + normalX,
                start.y + normalY
            );

            context.strokeStyle =
                "#ffffff";

            context.lineWidth = 8;

            context.stroke();


            // DRS 구간

            const drsStart =
                getTrackPosition(0.08);

            const drsEnd =
                getTrackPosition(0.23);

            context.beginPath();

            context.moveTo(
                drsStart.x,
                drsStart.y
            );

            context.lineTo(
                drsEnd.x,
                drsEnd.y
            );

            context.strokeStyle =
                "#25dfff";

            context.lineWidth = 8;

            context.stroke();

            context.fillStyle =
                "#25dfff";

            context.font =
                "bold 13px Arial";

            context.fillText(
                "DRS ZONE",
                drsStart.x,
                drsStart.y - 18
            );
        }


        // ---------------------------------------------
        // 차량 그리기
        // ---------------------------------------------

        function drawCar(
            vehicle,
            isPlayer = false
        ) {
            const position =
                getTrackPosition(
                    vehicle.progress
                );

            const lane =
                vehicle.lane || 0;

            const normalX =
                -Math.sin(
                    position.angle
                )
                * lane;

            const normalY =
                Math.cos(
                    position.angle
                )
                * lane;

            context.save();

            context.translate(
                position.x + normalX,
                position.y + normalY
            );

            context.rotate(
                position.angle
            );


            // 그림자

            context.fillStyle =
                "#00000088";

            context.fillRect(
                -15,
                -10,
                32,
                20
            );


            // 차체

            context.fillStyle =
                isPlayer
                    ? CONFIG.color
                    : vehicle.color;

            context.beginPath();

            context.moveTo(
                19,
                0
            );

            context.lineTo(
                8,
                -7
            );

            context.lineTo(
                -13,
                -8
            );

            context.lineTo(
                -19,
                -4
            );

            context.lineTo(
                -19,
                4
            );

            context.lineTo(
                -13,
                8
            );

            context.lineTo(
                8,
                7
            );

            context.closePath();
            context.fill();


            // 타이어

            context.fillStyle =
                "#050505";

            context.fillRect(
                -12,
                -12,
                7,
                5
            );

            context.fillRect(
                6,
                -10,
                7,
                4
            );

            context.fillRect(
                -12,
                7,
                7,
                5
            );

            context.fillRect(
                6,
                6,
                7,
                4
            );


            // 콕핏

            context.fillStyle =
                "#b9e9ff";

            context.fillRect(
                -1,
                -4,
                8,
                8
            );


            // 플레이어 표시

            if (isPlayer) {
                context.fillStyle =
                    "#ffffff";

                context.beginPath();

                context.moveTo(
                    0,
                    -20
                );

                context.lineTo(
                    -5,
                    -27
                );

                context.lineTo(
                    5,
                    -27
                );

                context.closePath();
                context.fill();
            }

            context.restore();
        }


        // ---------------------------------------------
        // 차량 업데이트
        // ---------------------------------------------

        function updatePlayer(
            deltaTime
        ) {
            if (
                !raceActive
                || raceFinished
            ) {
                return;
            }

            const stats =
                CONFIG.stats;

            const accelerationFactor =
                stats.acceleration / 70;

            let maximumSpeed =
                205
                + stats.top_speed
                * 1.17
                - stats.drag
                * 0.10;


            // 타이어 마모에 따른 그립 감소

            const wearRatio =
                (
                    100
                    - player.tyre
                )
                / 100;

            const currentGrip =
                (
                    stats.grip / 100
                )
                * (
                    1
                    - wearRatio * 0.58
                );


            // 가속과 제동

            if (keys["w"]) {
                player.speed +=
                    50
                    * accelerationFactor
                    * deltaTime;
            } else {
                player.speed -=
                    12
                    * deltaTime;
            }

            if (keys["s"]) {
                player.speed -=
                    92
                    * (
                        stats.braking / 70
                    )
                    * deltaTime;
            }


            // DRS

            const lapProgress =
                player.progress % 1;

            const inDrsZone =
                lapProgress > 0.08
                && lapProgress < 0.23;

            const drsActive =
                inDrsZone
                && keys["e"];

            if (drsActive) {
                maximumSpeed += 42;

                if (!player.lastDrs) {
                    player.drsUses += 1;
                    player.lastDrs = true;
                }
            } else {
                player.lastDrs = false;
            }


            // ERS

            const ersActive =
                keys["shift"]
                && player.ers > 0;

            if (ersActive) {
                player.speed +=
                    42
                    * deltaTime;

                maximumSpeed += 25;

                player.ers = Math.max(
                    0,
                    player.ers
                    - 12 * deltaTime
                );
            } else {
                player.ers = Math.min(
                    100,
                    player.ers
                    + 2.8 * deltaTime
                );
            }


            // 연료가 거의 없을 때 성능 감소

            if (player.fuel < 8) {
                maximumSpeed *= 0.82;
            }


            player.speed = Math.max(
                -30,
                Math.min(
                    maximumSpeed,
                    player.speed
                )
            );


            // 조향

            let steering = 0;

            if (keys["a"]) {
                steering -= 1;
            }

            if (keys["d"]) {
                steering += 1;
            }

            player.lane +=
                steering
                * (
                    40
                    + player.speed * 0.12
                )
                * deltaTime
                * (
                    0.6
                    + currentGrip
                );

            player.lane *=
                Math.pow(
                    0.93,
                    deltaTime * 10
                );


            // 트랙 이탈 패널티

            if (
                Math.abs(player.lane)
                > 52 * scale
            ) {
                player.speed *=
                    Math.pow(
                        0.83,
                        deltaTime * 6
                    );

                raceMessage.textContent =
                    "트랙 이탈 — 속도와 GRIP 감소";
            } else if (drsActive) {
                raceMessage.textContent =
                    "DRS ACTIVE";
            } else if (inDrsZone) {
                raceMessage.textContent =
                    "DRS AVAILABLE — E";
            } else if (ersActive) {
                raceMessage.textContent =
                    "ERS DEPLOY";
            } else {
                raceMessage.textContent =
                    "";
            }


            // 주행 진행

            player.progress +=
                (
                    player.speed
                    / 145000
                )
                * deltaTime
                * 60;


            // 랩 완료

            if (
                player.progress
                >= player.lap + 1
            ) {
                player.lap += 1;

                lapTimes.push(
                    performance.now()
                    - lapStartTime
                );

                lapStartTime =
                    performance.now();

                if (
                    player.lap
                    >= CONFIG.laps
                ) {
                    finishRace();
                }
            }


            // 연료 소모

            player.fuel = Math.max(
                0,
                player.fuel
                - (
                    0.05
                    + (
                        keys["w"]
                            ? 0.035
                            : 0
                    )
                )
                * deltaTime
            );


            // 타이어 마모

            let wearRate = 0.058;

            if (CONFIG.tire === "Soft") {
                wearRate = 0.09;
            } else if (
                CONFIG.tire === "Hard"
            ) {
                wearRate = 0.035;
            }

            player.tyre = Math.max(
                0,
                player.tyre
                - wearRate
                * (
                    stats.tire_wear
                    / 50
                )
                * deltaTime
            );


            player.topSpeed = Math.max(
                player.topSpeed,
                player.speed
            );


            // 자동 또는 수동 변속

            if (CONFIG.manual) {
                if (
                    keys["q"]
                    && !player.shiftUpPressed
                ) {
                    player.gear = Math.min(
                        8,
                        player.gear + 1
                    );

                    player.shiftUpPressed =
                        true;
                }

                if (!keys["q"]) {
                    player.shiftUpPressed =
                        false;
                }

                if (
                    keys["z"]
                    && !player.shiftDownPressed
                ) {
                    player.gear = Math.max(
                        1,
                        player.gear - 1
                    );

                    player.shiftDownPressed =
                        true;
                }

                if (!keys["z"]) {
                    player.shiftDownPressed =
                        false;
                }
            } else {
                player.gear = Math.max(
                    1,
                    Math.min(
                        8,
                        Math.ceil(
                            player.speed / 42
                        )
                    )
                );
            }


            // AI 업데이트

            aiCars.forEach(
                (ai, index) => {
                    const previousLap =
                        Math.floor(
                            ai.progress
                        );

                    let targetSpeed =
                        ai.speed;

                    const curveEffect =
                        Math.sin(
                            ai.progress
                            * trackPoints.length
                            * Math.PI
                        );

                    if (
                        Math.abs(curveEffect)
                        > 0.65
                    ) {
                        targetSpeed *=
                            0.72
                            + ai.cornering * 0.18;
                    }

                    targetSpeed *=
                        0.98
                        + ai.aggression * 0.025;

                    targetSpeed *=
                        1
                        + 0.012
                        * Math.sin(
                            performance.now()
                            / 1000
                            + index
                        );

                    ai.currentSpeed +=
                        (
                            targetSpeed
                            - ai.currentSpeed
                        )
                        * deltaTime
                        * ai.stability;

                    ai.progress +=
                        (
                            ai.currentSpeed
                            / 145000
                        )
                        * deltaTime
                        * 60;

                    if (
                        Math.floor(
                            ai.progress
                        )
                        > previousLap
                    ) {
                        ai.lap += 1;
                    }

                    ai.lane =
                        Math.sin(
                            ai.progress * 35
                            + index
                        )
                        * (
                            13
                            - ai.stability * 4
                        );
                }
            );


            const carsAhead =
                aiCars.filter(
                    ai =>
                        ai.progress
                        > player.progress
                ).length;

            player.overtakes = Math.max(
                player.overtakes,
                5 - carsAhead
            );


            if (keys["r"]) {
                window.location.reload();
            }
        }


        // ---------------------------------------------
        // HUD 업데이트
        // ---------------------------------------------

        function updateHud() {
            lapDisplay.textContent =
                `LAP ${
                    Math.min(
                        player.lap + 1,
                        CONFIG.laps
                    )
                } / ${CONFIG.laps}`;

            const position =
                1
                + aiCars.filter(
                    ai =>
                        ai.progress
                        > player.progress
                ).length;

            positionDisplay.textContent =
                `POSITION P${position}`;


            const elapsed =
                raceActive
                    ? performance.now()
                        - raceStartTime
                    : 0;

            const minutes =
                Math.floor(
                    elapsed / 60000
                );

            const seconds =
                (
                    (
                        elapsed % 60000
                    )
                    / 1000
                ).toFixed(3);

            timeDisplay.textContent =
                `${String(minutes).padStart(2, "0")}:`
                + `${String(seconds).padStart(6, "0")}`;


            speedDisplay.textContent =
                Math.max(
                    0,
                    Math.round(
                        player.speed
                    )
                );


            const rpmRatio =
                Math.min(
                    100,
                    (
                        (
                            Math.max(
                                0,
                                player.speed
                            )
                            % 42
                        )
                        / 42
                    )
                    * 100
                );

            rpmDisplay.textContent =
                Math.round(
                    5000
                    + rpmRatio * 70
                );

            rpmBar.style.width =
                `${rpmRatio}%`;


            gearDisplay.textContent =
                player.speed < 0
                    ? "R"
                    : player.gear;


            ersDisplay.textContent =
                `${player.ers.toFixed(0)}%`;

            ersBar.style.width =
                `${player.ers}%`;


            const lapProgress =
                player.progress % 1;

            const inDrsZone =
                lapProgress > 0.08
                && lapProgress < 0.23;

            if (
                inDrsZone
                && keys["e"]
            ) {
                drsDisplay.textContent =
                    "ACTIVE";

                drsDisplay.style.color =
                    "#25dfff";
            } else if (inDrsZone) {
                drsDisplay.textContent =
                    "READY";

                drsDisplay.style.color =
                    "#ffe500";
            } else {
                drsDisplay.textContent =
                    "LOCKED";

                drsDisplay.style.color =
                    "#ffffff";
            }


            tyreDisplay.textContent =
                `${player.tyre.toFixed(0)}%`;

            tyreBar.style.width =
                `${player.tyre}%`;


            fuelDisplay.textContent =
                `${player.fuel.toFixed(0)}%`;

            fuelBar.style.width =
                `${player.fuel}%`;
        }


        // ---------------------------------------------
        // 레이스 종료
        // ---------------------------------------------

        function finishRace() {
            raceFinished = true;

            const resultRows = [
                {
                    name: "YOU",
                    progress:
                        player.progress
                },

                ...aiCars.map(
                    ai => ({
                        name: ai.name,
                        progress:
                            ai.progress
                    })
                )
            ].sort(
                (
                    first,
                    second
                ) =>
                    second.progress
                    - first.progress
            );


            const finalPosition =
                resultRows.findIndex(
                    result =>
                        result.name
                        === "YOU"
                )
                + 1;


            const fastestLap =
                lapTimes.length > 0
                    ? Math.min(
                        ...lapTimes
                    )
                    : 0;

            const fastestMinutes =
                Math.floor(
                    fastestLap / 60000
                );

            const fastestSeconds =
                (
                    (
                        fastestLap % 60000
                    )
                    / 1000
                )
                .toFixed(3)
                .padStart(
                    6,
                    "0"
                );


            finishPanel.classList.remove(
                "hidden"
            );

            finishPanel.innerHTML = `
                <div
                    style="
                        color:#e10600;
                        font-weight:900;
                        letter-spacing:3px;
                    "
                >
                    RACE FINISHED
                </div>

                <h1>P${finalPosition}</h1>

                <h3>
                    FASTEST LAP
                    ${fastestMinutes}:${fastestSeconds}
                </h3>

                <h3>
                    TOP SPEED
                    ${player.topSpeed.toFixed(0)}
                    km/h
                </h3>

                <p>
                    추월 ${player.overtakes}회 ·
                    DRS 사용 ${player.drsUses}회 ·
                    타이어 잔량
                    ${player.tyre.toFixed(0)}% ·
                    연료 잔량
                    ${player.fuel.toFixed(0)}%
                </p>

                <hr>

                ${
                    resultRows.map(
                        (
                            result,
                            index
                        ) => `
                            <p>
                                <b>
                                    P${index + 1}
                                </b>
                                &nbsp;
                                ${result.name}
                            </p>
                        `
                    ).join("")
                }

                <button
                    onclick="window.location.reload()"
                >
                    다시 달리기
                </button>
            `;
        }


        // ---------------------------------------------
        // 메인 루프
        // ---------------------------------------------

        function gameLoop(
            currentTime
        ) {
            const deltaTime =
                Math.min(
                    0.04,
                    (
                        currentTime
                        - lastFrameTime
                    )
                    / 1000
                );

            lastFrameTime =
                currentTime;

            context.clearRect(
                0,
                0,
                width,
                height
            );

            drawTrack();

            aiCars.forEach(
                ai => drawCar(
                    ai,
                    false
                )
            );

            drawCar(
                player,
                true
            );

            updatePlayer(
                deltaTime
            );

            updateHud();

            requestAnimationFrame(
                gameLoop
            );
        }

        requestAnimationFrame(
            gameLoop
        );
    </script>
</body>
</html>
"""

    return race_html.replace(
        "__RACE_CONFIG__",
        json.dumps(config),
    )


# =========================================================
# 레이스 페이지
# =========================================================

def render_race():
    st.title("레이스 · 직접 운전")

    if not st.session_state.race_on:
        st.caption(
            "트랙, 랩 수, 변속 방식을 선택한 뒤 "
            "레이스를 시작하세요."
        )

        track_column, lap_column, gear_column = st.columns(3)

        with track_column:
            selected_track = st.selectbox(
                "트랙 선택",
                [
                    "고속 서킷",
                    "테크니컬 서킷",
                    "밸런스 서킷",
                ],
            )

        with lap_column:
            selected_laps = st.selectbox(
                "랩 수",
                [3, 5, 7],
                index=1,
            )

        with gear_column:
            manual_gear = st.toggle(
                "수동 기어",
                value=False,
                help=(
                    "활성화하면 Q로 업시프트하고 "
                    "Z로 다운시프트합니다."
                ),
            )

        st.markdown(
            f"""
            <div class="panel">
                <div class="eyebrow">
                    현재 차량 설정
                </div>

                <h3>AF-01 RACE SETUP</h3>

                <span class="tag">
                    {st.session_state.parts["tires"]}
                </span>

                <span class="tag">
                    {st.session_state.parts["engine"]}
                </span>

                <span class="tag">
                    {st.session_state.parts["front_wing"]}
                </span>

                <span class="tag">
                    {st.session_state.parts["rear_wing"]}
                </span>

                <p>
                    W 가속 · S 브레이크 · A/D 조향 ·
                    SHIFT ERS · E DRS · Q/Z 수동 변속
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        setup_stats = calculate_stats()

        setup_columns = st.columns(4)

        setup_columns[0].metric(
            "TOP SPEED",
            setup_stats["top_speed"],
        )

        setup_columns[1].metric(
            "CORNERING",
            setup_stats["cornering"],
        )

        setup_columns[2].metric(
            "GRIP",
            setup_stats["grip"],
        )

        setup_columns[3].metric(
            "TIRE WEAR",
            setup_stats["tire_wear"],
        )

        if st.button(
            "RACE START",
            use_container_width=True,
        ):
            st.session_state.race_config = (
                selected_track,
                selected_laps,
                manual_gear,
            )

            st.session_state.race_on = True
            st.rerun()

    else:
        selected_track, selected_laps, manual_gear = (
            st.session_state.race_config
        )

        if st.button(
            "← 레이스 설정으로 돌아가기"
        ):
            st.session_state.race_on = False
            st.rerun()

        components.html(
            build_race_html(
                selected_track,
                selected_laps,
                manual_gear,
            ),
            height=790,
            scrolling=False,
        )

        st.info(
            "레이스 화면을 한 번 클릭한 뒤 키보드로 조작하세요. "
            "브라우저가 키 입력을 받으려면 게임 화면에 포커스가 "
            "있어야 합니다."
        )


# =========================================================
# 팀 매칭
# =========================================================

def calculate_similarity(
    car_profile,
    team_profile,
    keys,
):
    difference = math.sqrt(
        sum(
            (
                car_profile[key]
                - team_profile[key]
            ) ** 2
            for key in keys
        )
        / len(keys)
    )

    return max(
        0,
        min(
            100,
            round(
                100
                - difference * 1.25
            ),
        ),
    )


def render_team_match():
    current_stats = calculate_stats()

    matching_stats = [
        "top_speed",
        "downforce",
        "grip",
        "stability",
        "cornering",
        "tire_wear",
    ]

    similarity_scores = {
        team_name: calculate_similarity(
            current_stats,
            profile,
            matching_stats,
        )
        for team_name, profile
        in TEAM_PROFILES.items()
    }

    best_team = max(
        similarity_scores,
        key=similarity_scores.get,
    )

    st.title(
        "팀 매칭 · 차량 설계 DNA"
    )

    vehicle_column, result_column = st.columns(
        [1.3, 0.7]
    )

    with vehicle_column:
        render_3d_car(
            height=460
        )

    with result_column:
        st.markdown(
            f"""
            <div class="panel">
                <div class="eyebrow">
                    가장 가까운 설계 철학
                </div>

                <h1>{best_team}</h1>

                <h2 style="color:#e10600">
                    {similarity_scores[best_team]}% 일치
                </h2>

                <p>
                    실제 시즌 성능이 아닌 게임에서 정의한
                    가상의 팀 설계 성향입니다.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        closest_stats = sorted(
            matching_stats,
            key=lambda stat: abs(
                current_stats[stat]
                - TEAM_PROFILES[best_team][stat]
            ),
        )[:3]

        st.subheader(
            "왜 이 팀과 비슷한가요?"
        )

        for stat in closest_stats:
            st.write(
                f"✓ **{LABELS[stat]}** 성향이 유사합니다. "
                f"내 차량 {current_stats[stat]} / "
                f"팀 기준 {TEAM_PROFILES[best_team][stat]}"
            )

        st.subheader(
            "전체 팀 유사도"
        )

        for team_name, score in sorted(
            similarity_scores.items(),
            key=lambda item: -item[1],
        ):
            st.progress(
                score / 100,
                text=f"{team_name} · {score}%",
            )


# =========================================================
# 레이싱 성향 테스트
# =========================================================

PSYCHOLOGY_QUESTIONS = [
    (
        "추월 기회가 보이면 어떻게 행동하나요?",
        [
            ("즉시 공격한다", "risk"),
            ("상대의 움직임을 분석한다", "precision"),
            ("상대의 실수를 기다린다", "strategy"),
            ("안전하게 순위를 유지한다", "stability"),
        ],
    ),
    (
        "레이스에서 가장 중요하다고 생각하는 것은?",
        [
            ("압도적인 최고속도", "speed"),
            ("정확한 코너링", "precision"),
            ("안정적인 운영", "stability"),
            ("과감한 전략", "strategy"),
        ],
    ),
    (
        "새로운 기술 규정이 발표됐습니다.",
        [
            ("극단적인 신기술을 개발한다", "innovation"),
            ("검증된 방식을 개선한다", "stability"),
            ("시뮬레이션으로 정답을 찾는다", "precision"),
            ("규정의 허점을 전략적으로 찾는다", "strategy"),
        ],
    ),
    (
        "레이스 마지막 랩에서 앞차와 0.5초 차이입니다.",
        [
            ("한계를 넘어 공격한다", "risk"),
            ("직선 최고속도를 활용한다", "speed"),
            ("실수 없이 정확히 압박한다", "precision"),
            ("상대가 흔들릴 때까지 기다린다", "strategy"),
        ],
    ),
    (
        "타이어 상태가 예상보다 나쁩니다.",
        [
            ("계속 최대 속도로 달린다", "risk"),
            ("페이스를 낮추고 관리한다", "stability"),
            ("빠른 피트스톱 전략을 시도한다", "strategy"),
            ("새로운 주행법을 시험한다", "innovation"),
        ],
    ),
    (
        "가장 만족스러운 승리는 무엇인가요?",
        [
            ("최고속도로 압도한 승리", "speed"),
            ("0.001초 차이의 정교한 승리", "precision"),
            ("피트 전략으로 뒤집은 승리", "strategy"),
            ("새로운 기술로 만든 데뷔 승리", "innovation"),
        ],
    ),
    (
        "팀 동료와 경쟁하게 됐습니다.",
        [
            ("정면으로 승부한다", "risk"),
            ("데이터를 공유하며 함께 발전한다", "stability"),
            ("상대의 약점을 분석한다", "strategy"),
            ("완전히 새로운 방식을 개발한다", "innovation"),
        ],
    ),
    (
        "당신이 원하는 차량의 성격은?",
        [
            ("직선에서 가장 빠른 차량", "speed"),
            ("어떤 상황에서도 안정적인 차량", "stability"),
            ("조작이 매우 정확한 차량", "precision"),
            ("기존과 완전히 다른 혁신적인 차량", "innovation"),
        ],
    ),
]


PSYCHOLOGY_TEAMS = {
    "크림슨 에이펙스": {
        "speed": 90,
        "risk": 86,
        "stability": 55,
        "strategy": 65,
        "innovation": 72,
        "precision": 70,
    },
    "실버 벡터": {
        "speed": 72,
        "risk": 45,
        "stability": 88,
        "strategy": 90,
        "innovation": 68,
        "precision": 93,
    },
    "옵시디언 벨로시티": {
        "speed": 94,
        "risk": 75,
        "stability": 62,
        "strategy": 58,
        "innovation": 82,
        "precision": 68,
    },
    "에메랄드 인듀어런스": {
        "speed": 62,
        "risk": 30,
        "stability": 95,
        "strategy": 88,
        "innovation": 55,
        "precision": 84,
    },
}


def render_psychology_test():
    st.title(
        "레이싱 성향 테스트"
    )

    st.caption(
        "차량 설계 분석과 별개로, 운전과 전략에 관한 "
        "선택을 바탕으로 드라이버 성향을 분석합니다."
    )

    answers = {}

    with st.form(
        "psychology_form"
    ):
        for index, (
            question,
            options,
        ) in enumerate(
            PSYCHOLOGY_QUESTIONS
        ):
            option_labels = [
                label
                for label, category
                in options
            ]

            answers[index] = st.radio(
                f"{index + 1:02}. {question}",
                option_labels,
                horizontal=True,
                key=f"psychology_question_{index}",
            )

        submitted = st.form_submit_button(
            "레이싱 성향 분석",
            use_container_width=True,
        )

    if submitted:
        profile = {
            "speed": 30,
            "risk": 30,
            "stability": 30,
            "strategy": 30,
            "innovation": 30,
            "precision": 30,
        }

        for index, (
            question,
            options,
        ) in enumerate(
            PSYCHOLOGY_QUESTIONS
        ):
            selected_label = answers[index]

            selected_category = next(
                category
                for label, category
                in options
                if label == selected_label
            )

            profile[selected_category] += 18

        profile = {
            key: min(
                99,
                value,
            )
            for key, value
            in profile.items()
        }

        score_keys = list(profile)

        team_scores = {
            team_name: calculate_similarity(
                profile,
                team_profile,
                score_keys,
            )
            for team_name, team_profile
            in PSYCHOLOGY_TEAMS.items()
        }

        recommended_team = max(
            team_scores,
            key=team_scores.get,
        )

        st.session_state.psychology_result = {
            "profile": profile,
            "team": recommended_team,
            "score": team_scores[
                recommended_team
            ],
        }

    if (
        "psychology_result"
        in st.session_state
    ):
        result = (
            st.session_state.psychology_result
        )

        profile = result["profile"]
        recommended_team = result["team"]
        match_score = result["score"]

        profile_column, team_column = st.columns(
            2
        )

        with profile_column:
            st.subheader(
                "YOUR RACING PERSONALITY"
            )

            for category, value in profile.items():
                st.progress(
                    value / 100,
                    text=(
                        f"{category.upper()} · "
                        f"{value}"
                    ),
                )

        with team_column:
            if (
                profile["strategy"]
                + profile["stability"]
                > profile["risk"]
                + profile["speed"]
            ):
                personality_summary = (
                    "정교한 전략과 안정적인 운영을 "
                    "중요하게 생각하는 드라이버입니다."
                )
            else:
                personality_summary = (
                    "속도와 과감한 도전을 중요하게 "
                    "생각하는 공격적인 드라이버입니다."
                )

            st.markdown(
                f"""
                <div class="panel">
                    <div class="eyebrow">
                        YOUR TEAM MATCH
                    </div>

                    <h1>{recommended_team}</h1>

                    <h2 style="color:#e10600">
                        {match_score}% 일치
                    </h2>

                    <p>
                        {personality_summary}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# =========================================================
# 앱 실행
# =========================================================

navigation()

PAGE_RENDERERS = {
    "홈": render_home,
    "차고": render_garage,
    "튜토리얼": render_tutorial,
    "공력 테스트": render_aero_test,
    "레이스": render_race,
    "팀 매칭": render_team_match,
    "성향 테스트": render_psychology_test,
}

try:
    selected_renderer = PAGE_RENDERERS.get(
        st.session_state.page,
        render_home,
    )

    selected_renderer()

except Exception as error:
    st.error(
        "Race Control이 오류를 감지했습니다. "
        "홈으로 돌아가거나 페이지를 새로고침해 주세요."
    )

    st.exception(error)


st.markdown(
    """
    <hr>

    <small class="muted">
        MY F1 GARAGE · 실제 특정 F1 팀, 차량 또는 로고를
        복제하지 않은 오리지널 레이싱 게임입니다.
    </small>
    """,
    unsafe_allow_html=True,
)
