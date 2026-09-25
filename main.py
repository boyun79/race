import math, random, time
from dataclasses import dataclass
import streamlit as st

st.set_page_config(page_title="APEX FORGE", page_icon="🏎️", layout="wide", initial_sidebar_state="collapsed")

STATS=["top_speed","acceleration","downforce","grip","stability","braking","cornering","drag","tire_wear"]
LABELS={"top_speed":"TOP SPEED","acceleration":"ACCELERATION","downforce":"DOWNFORCE","grip":"GRIP","stability":"STABILITY","braking":"BRAKING","cornering":"CORNERING","drag":"DRAG","tire_wear":"TIRE WEAR"}
BASE={k:55 for k in STATS}; BASE.update(drag=45,tire_wear=45)
PARTS={
"engine":{
 "Velocity V10":{"top_speed":16,"acceleration":6,"stability":-5,"drag":3},
 "Pulse Hybrid":{"acceleration":15,"top_speed":6,"stability":2,"tire_wear":2},
 "Endurance-X":{"stability":12,"acceleration":5,"top_speed":-4,"tire_wear":-4}},
"front_wing":{
 "Falcon High-Load":{"downforce":14,"cornering":10,"drag":9,"top_speed":-4},
 "Razor Low-Drag":{"top_speed":9,"drag":-12,"downforce":-7,"cornering":-5},
 "Vector Balanced":{"downforce":7,"cornering":6,"drag":3,"stability":3}},
"rear_wing":{
 "Monaco Blade":{"downforce":14,"grip":5,"drag":10,"top_speed":-5},
 "Monza Sprint":{"top_speed":10,"drag":-11,"downforce":-8,"stability":-3},
 "Apex Dualplane":{"downforce":7,"stability":6,"drag":4}},
"floor":{
 "Groundforce Venturi":{"downforce":15,"cornering":8,"drag":5,"stability":-2},
 "Streamline Diffuser":{"drag":-9,"top_speed":7,"downforce":3},
 "Stable Channel":{"stability":10,"downforce":7,"cornering":4,"drag":4}},
"tires":{
 "Soft":{"grip":16,"cornering":10,"acceleration":5,"tire_wear":17},
 "Medium":{"grip":9,"cornering":6,"tire_wear":7,"stability":3},
 "Hard":{"grip":3,"stability":7,"tire_wear":-12,"top_speed":2}},
"suspension":{
 "Reactive Stiff":{"cornering":12,"stability":-4,"grip":5,"tire_wear":6},
 "Adaptive Balance":{"stability":9,"cornering":7,"tire_wear":-2},
 "Compliant Enduro":{"stability":12,"grip":5,"cornering":-3,"tire_wear":-9}},
"brakes":{
 "Carbon Attack":{"braking":16,"stability":-3,"tire_wear":5},
 "Progressive Control":{"braking":10,"stability":8,"cornering":3},
 "Endurance Ceramic":{"braking":7,"stability":5,"tire_wear":-7}}
}
DEFAULT={k:list(v)[0] for k,v in PARTS.items()}
TEAMS={
 "Crimson Apex":{"top_speed":82,"downforce":76,"grip":72,"stability":68,"cornering":78,"tire_wear":55},
 "Silver Vector":{"top_speed":74,"downforce":80,"grip":78,"stability":86,"cornering":82,"tire_wear":38},
 "Obsidian Velocity":{"top_speed":91,"downforce":62,"grip":66,"stability":70,"cornering":64,"tire_wear":50},
 "Emerald Endurance":{"top_speed":70,"downforce":72,"grip":75,"stability":90,"cornering":74,"tire_wear":28},
 "Neon Nova":{"top_speed":79,"downforce":71,"grip":84,"stability":64,"cornering":86,"tire_wear":63}
}
PSY_TEAMS={
 "Crimson Apex":{"speed":90,"risk":85,"stability":55,"strategy":65,"innovation":70,"precision":72},
 "Silver Vector":{"speed":72,"risk":45,"stability":88,"strategy":90,"innovation":68,"precision":92},
 "Obsidian Velocity":{"speed":92,"risk":72,"stability":62,"strategy":58,"innovation":82,"precision":68},
 "Emerald Endurance":{"speed":62,"risk":30,"stability":94,"strategy":88,"innovation":55,"precision":84},
 "Neon Nova":{"speed":75,"risk":78,"stability":60,"strategy":72,"innovation":95,"precision":70}
}
AI=[
 ("NOVA-01","Aggressive",{"top_speed":84,"acceleration":82,"downforce":66,"grip":70,"stability":61,"braking":72,"cornering":69,"drag":39,"tire_wear":61}),
 ("VECTOR-7","Corner Specialist",{"top_speed":71,"acceleration":74,"downforce":88,"grip":86,"stability":79,"braking":83,"cornering":91,"drag":59,"tire_wear":53}),
 ("ONYX-12","Straight-line Specialist",{"top_speed":93,"acceleration":87,"downforce":57,"grip":65,"stability":67,"braking":71,"cornering":62,"drag":28,"tire_wear":48}),
 ("AEGIS-4","Defensive",{"top_speed":73,"acceleration":69,"downforce":74,"grip":76,"stability":92,"braking":82,"cornering":77,"drag":47,"tire_wear":32}),
 ("PULSE-9","Balanced",{"top_speed":79,"acceleration":78,"downforce":77,"grip":79,"stability":78,"braking":78,"cornering":79,"drag":45,"tire_wear":46})]

CSS='''<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=Rajdhani:wght@500;700&display=swap');
.stApp{background:radial-gradient(circle at 75% 0,#241014 0,#090a0d 35%,#050608 100%);color:#f5f5f5;font-family:Rajdhani,sans-serif}.block-container{max-width:1450px;padding:1.1rem 2rem 4rem}.stButton>button{background:linear-gradient(135deg,#ef233c,#9d0208);color:white;border:0;border-radius:3px;font-family:'Barlow Condensed';font-weight:800;letter-spacing:1.5px;min-height:44px;box-shadow:0 0 20px #ef233c33}.stButton>button:hover{border:1px solid #ff5a69;transform:translateY(-1px)}
[data-testid="stSidebar"]{background:#08090c}.panel{background:linear-gradient(145deg,#15171d,#0b0c10);border:1px solid #2b2e36;border-left:3px solid #ef233c;padding:18px;border-radius:5px;box-shadow:0 14px 45px #0008;margin:8px 0}.hero{padding:42px 30px;background:linear-gradient(100deg,#090a0ddd,#090a0d88),repeating-linear-gradient(135deg,#161820 0,#161820 2px,#0c0d11 2px,#0c0d11 14px);border-bottom:4px solid #ef233c;clip-path:polygon(0 0,100% 0,96% 100%,0 100%)}
h1,h2,h3{font-family:'Barlow Condensed';font-style:italic;letter-spacing:1px}.logo{font:900 64px 'Barlow Condensed';font-style:italic;line-height:.8}.logo span,.red{color:#ef233c}.eyebrow{font:700 13px 'Barlow Condensed';letter-spacing:4px;color:#a4a7af}.metric{font:900 38px 'Barlow Condensed';font-style:italic}.muted{color:#9296a1}.tag{display:inline-block;padding:4px 9px;background:#ef233c22;color:#ff6373;border:1px solid #ef233c66;margin:2px;font-size:12px}.bar{height:8px;background:#262932;overflow:hidden;transform:skew(-12deg);margin:4px 0 12px}.fill{height:100%;background:linear-gradient(90deg,#ef233c,#ffb703);box-shadow:0 0 14px #ef233c}.telemetry{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}.tele{background:#090a0d;border-top:2px solid #ef233c;padding:10px}.tele b{font:800 24px 'Barlow Condensed'}.carbox{background:radial-gradient(ellipse,#222630,#08090c 65%);border:1px solid #30333b;padding:16px;text-align:center;overflow:hidden}.menu-card{min-height:95px;background:#111319;border:1px solid #292c33;border-top:3px solid #ef233c;padding:14px}.rank1{color:#ffcc00}.small{font-size:12px}.flow{stroke-dasharray:12 8;animation:dash 1.4s linear infinite}@keyframes dash{to{stroke-dashoffset:-40}} div[data-baseweb="select"]>div{background:#111319;border-color:#343740} .stProgress>div>div{background:#ef233c}</style>'''
st.markdown(CSS,unsafe_allow_html=True)

def init():
 ss=st.session_state
 if "page" not in ss:ss.page="HOME"
 if "parts" not in ss:ss.parts=DEFAULT.copy()
 if "color" not in ss:ss.color="#EF233C"
 if "race" not in ss:ss.race=None
 if "test" not in ss:ss.test=None
init()

def calc(parts=None):
 parts=parts or st.session_state.parts;s=BASE.copy()
 for cat,name in parts.items():
  for k,v in PARTS[cat][name].items():s[k]+=v
 return {k:max(10,min(99,round(v))) for k,v in s.items()}

def nav():
 cols=st.columns([1.7,1,1,1,1,1,1])
 cols[0].markdown('<div style="font:900 28px Barlow Condensed;font-style:italic">APEX <span class="red">FORGE</span></div>',unsafe_allow_html=True)
 for c,(label,p) in zip(cols[1:],[('HOME','HOME'),('GARAGE','GARAGE'),('CFD LAB','TEST'),('RACE','RACE'),('TEAM MATCH','MATCH'),('PSYCHOLOGY','PSY')]):
  if c.button(label,use_container_width=True,key='nav'+p):st.session_state.page=p;st.rerun()

def car_svg(stats,wide=True):
 c=st.session_state.color; wing=18+stats['downforce']//7; tire="#151515"
 return f'''<svg viewBox="0 0 720 270" width="100%" aria-label="original racing car">
 <defs><linearGradient id="body" x2="1"><stop stop-color="{c}"/><stop offset=".55" stop-color="#fff"/><stop offset=".6" stop-color="{c}"/><stop offset="1" stop-color="#68000b"/></linearGradient><filter id="gl"><feGaussianBlur stdDeviation="5"/></filter></defs>
 <ellipse cx="365" cy="229" rx="290" ry="20" fill="#ef233c" opacity=".18" filter="url(#gl)"/>
 <g stroke="#090909" stroke-width="6"><rect x="90" y="55" width="45" height="90" rx="15" fill="{tire}"/><rect x="90" y="165" width="45" height="90" rx="15" fill="{tire}"/><rect x="560" y="55" width="45" height="90" rx="15" fill="{tire}"/><rect x="560" y="165" width="45" height="90" rx="15" fill="{tire}"/></g>
 <path d="M105 102 L215 105 L310 70 L500 95 L640 117 L650 157 L500 175 L310 200 L215 165 L105 168 Z" fill="url(#body)" stroke="#f5f5f5" stroke-width="2"/>
 <path d="M265 106 Q360 68 460 105 L438 166 Q360 189 275 163Z" fill="#101319"/><path d="M315 107 Q360 87 405 108 L397 151 Q360 165 322 150Z" fill="#45a3bf" opacity=".65"/>
 <rect x="625" y="90" width="{wing*2}" height="96" fill="{c}"/><rect x="55" y="88" width="{wing*2}" height="106" fill="{c}"/><text x="335" y="142" fill="white" font-size="26" font-family="sans-serif" font-weight="900">AF-01</text></svg>'''

def gauges(s, keys=None):
 keys=keys or STATS
 for k in keys:
  val=s[k]; color="#29d98f" if (k in ['drag','tire_wear'] and val<45) or (k not in ['drag','tire_wear'] and val>=75) else "#ef233c"
  st.markdown(f'<div><span class="eyebrow">{LABELS[k]}</span><span style="float:right;font-weight:800">{val}</span><div class="bar"><div class="fill" style="width:{val}%;background:{color}"></div></div></div>',unsafe_allow_html=True)

def home():
 s=calc();st.markdown('''<div class="hero"><div class="eyebrow">ORIGINAL MOTORSPORT ENGINEERING SIM</div><div class="logo">BUILD. TEST. <span>RACE.</span></div><p class="muted">당신의 설계 철학이 랩타임이 됩니다. 머신을 제작하고, 공기 흐름을 검증하고, AI 라이벌을 추월하세요.</p></div>''',unsafe_allow_html=True)
 st.markdown(car_svg(s),unsafe_allow_html=True)
 a,b,c=st.columns([1.2,1,1]);
 with a:
  st.markdown('<div class="panel"><div class="eyebrow">NEXT SESSION</div><h2>01 / CAR GARAGE</h2><p>7개 핵심 파츠를 조합해 AF-01을 완성하세요.</p></div>',unsafe_allow_html=True)
  if st.button('ENTER GARAGE  →',use_container_width=True):st.session_state.page='GARAGE';st.rerun()
 with b:
  st.markdown('<div class="panel"><div class="eyebrow">QUICK START</div><h2>TUTORIAL</h2><p>설계부터 팀 분석까지 5단계 브리핑.</p></div>',unsafe_allow_html=True)
  if st.button('OPEN BRIEFING',use_container_width=True):st.session_state.page='TUTORIAL';st.rerun()
 with c:
  st.markdown(f'<div class="panel"><div class="eyebrow">CURRENT BUILD</div><div class="metric">{sum(s.values())//len(s)} <small>OVR</small></div><span class="tag">{st.session_state.parts["tires"]}</span><span class="tag">{st.session_state.parts["engine"]}</span></div>',unsafe_allow_html=True)

def tutorial():
 st.title('TUTORIAL // RACE CONTROL BRIEFING')
 steps=[('01','SELECT PARTS','엔진·윙·플로어·타이어·서스펜션·브레이크를 선택합니다.'),('02','READ TELEMETRY','장점에는 반드시 대가가 있습니다. 성능 게이지와 트레이드오프를 확인하세요.'),('03','CFD / TEST TRACK','공기 흐름과 예상 랩타임을 검증하고 필요하면 다시 셋업합니다.'),('04','RACE AI','서로 다른 머신과 운전 성향을 가진 5대의 AI와 5랩을 경쟁합니다.'),('05','FIND YOUR TEAM','차량 설계 성향 또는 심리 성향으로 오리지널 팀과 매칭합니다.')]
 for n,t,d in steps:st.markdown(f'<div class="panel"><span class="red metric">{n}</span>　<b>{t}</b><br><span class="muted">{d}</span></div>',unsafe_allow_html=True)
 if st.button('START ENGINE — GO TO GARAGE'):st.session_state.page='GARAGE';st.rerun()

def garage():
 st.title('CAR GARAGE // AF-01 BUILD BAY'); left,right=st.columns([1,1.25])
 with left:
  for cat,opts in PARTS.items():
   names=list(opts); current=st.session_state.parts[cat]
   pick=st.selectbox(cat.upper().replace('_',' / '),names,index=names.index(current),key='sel'+cat)
   st.session_state.parts[cat]=pick
   delta=opts[pick]; st.caption(' · '.join([f"{LABELS[k]} {'+' if v>0 else ''}{v}" for k,v in delta.items()]))
  st.session_state.color=st.color_picker('TEAM COLOR',st.session_state.color)
 with right:
  s=calc();st.markdown('<div class="carbox">'+car_svg(s)+'</div>',unsafe_allow_html=True)
  c1,c2=st.columns(2)
  with c1:gauges(s,STATS[:5])
  with c2:gauges(s,STATS[5:])
  st.info('DRAG와 TIRE WEAR는 낮을수록 유리합니다. 모든 수치는 선택한 파츠 보정치의 합으로 계산됩니다.')
  if st.button('LOCK BUILD & OPEN CFD LAB',use_container_width=True):st.session_state.page='TEST';st.rerun()

def lap_model(s,noise=0):
 straight=0.34*s['top_speed']+0.18*s['acceleration']-0.12*s['drag']
 fast=0.24*s['downforce']+0.22*s['cornering']; slow=0.18*s['grip']+0.14*s['braking']; control=.12*s['stability']-.08*s['tire_wear']
 score=straight+fast+slow+control
 return 102-score*.19+noise

def testlab():
 s=calc();st.title('TEST TRACK // CFD LAB'); a,b=st.columns([1.35,1])
 with a:
  st.markdown(f'''<div class="panel"><div class="eyebrow">AIRFLOW VISUALIZATION</div><svg viewBox="0 0 800 330" width="100%"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#48cae4"/></marker></defs><g fill="none" stroke="#48cae4" stroke-width="3" opacity=".8" marker-end="url(#a)"><path class="flow" d="M10 70 Q230 65 360 120 Q580 180 790 90"/><path class="flow" d="M10 145 Q250 140 390 155 Q600 165 790 150"/><path class="flow" d="M10 230 Q240 220 360 190 Q600 130 790 230"/></g><g transform="translate(100 70) scale(.75)">{car_svg(s)}</g></svg><div class="telemetry"><div class="tele">CL<b>{s['downforce']/50:.2f}</b></div><div class="tele">CD<b>{s['drag']/100:.2f}</b></div><div class="tele">FLOW SEP<b>{max(3,round((s['drag']-s['stability']/3)/2))}%</b></div><div class="tele">VORTEX<b>{round((s['downforce']+s['cornering'])/2)}</b></div></div></div>''',unsafe_allow_html=True)
 with b:
  st.subheader('AERO INTERPRETATION');
  st.write(f"• 전후 윙과 플로어가 **{s['downforce']} DF**를 생성합니다.")
  st.write(f"• 항력 지수 **{s['drag']}** — {'직선 효율 우수' if s['drag']<45 else '코너 성능과 맞바꾼 높은 저항'}")
  st.write(f"• 압력 분포: 프론트 {round(s['downforce']*.47)} / 리어 {round(s['downforce']*.53)}")
  st.write(f"• 흐름 박리 위험: {'LOW' if s['stability']>70 else 'MEDIUM'}")
  if st.button('RUN 3-LAP TEST',use_container_width=True):
   rng=random.Random(sum(s.values())+s['drag']); laps=[lap_model(s,rng.uniform(-.28,.28)+i*s['tire_wear']*.004) for i in range(3)];st.session_state.test=laps
  if st.session_state.test:
   laps=st.session_state.test
   for i,x in enumerate(laps):st.metric(f'LAP {i+1}',f'{x:.3f}s',f'{x-min(laps):+.3f}s')
   st.success(f'BEST {min(laps):.3f}s · 예상 최고속도 {238+s["top_speed"]*.92:.0f} km/h')
  if st.button('PROCEED TO RACE',use_container_width=True):st.session_state.page='RACE';st.rerun()

def race_sim():
 user=calc(); grid=[('YOU','Adaptive',user)]+AI; results=[]
 seed=sum(user.values())+sum(ord(x) for x in st.session_state.color);rng=random.Random(seed)
 for name,style,s in grid:
  laps=[]
  style_bonus={'Aggressive':-.18,'Defensive':.12,'Balanced':0,'Corner Specialist':-.10,'Straight-line Specialist':-.06,'Adaptive':0}[style]
  for l in range(5):
   wear=max(0,l*s['tire_wear']*.012); consistency=(100-s['stability'])*.006
   laps.append(lap_model(s,style_bonus+wear+rng.uniform(-consistency,consistency)))
  results.append({'name':name,'style':style,'laps':laps,'total':sum(laps),'fast':min(laps),'top':238+s['top_speed']*.92,'avg':188+(s['top_speed']+s['cornering'])*.24})
 return sorted(results,key=lambda x:x['total'])

def race():
 s=calc();st.title('RACE // NIGHT CIRCUIT · 5 LAPS')
 st.markdown('<div class="telemetry">'+''.join([f'<div class="tele"><span class="eyebrow">{LABELS[k]}</span><br><b>{s[k]}</b></div>' for k in ['top_speed','acceleration','downforce','grip']])+'</div>',unsafe_allow_html=True)
 st.markdown(car_svg(s),unsafe_allow_html=True)
 if st.button('● START RACE',use_container_width=True):st.session_state.race=race_sim()
 if st.session_state.race:
  r=st.session_state.race; userpos=next(i+1 for i,x in enumerate(r) if x['name']=='YOU'); leader=r[0]
  st.markdown(f'<div class="panel"><div class="eyebrow">CHEQUERED FLAG</div><div class="logo">P<span>{userpos}</span></div><div>GAP TO LEADER　{next(x for x in r if x["name"]=="YOU")["total"]-leader["total"]:+.3f}s</div></div>',unsafe_allow_html=True)
  for i,x in enumerate(r):
   st.markdown(f'<div class="panel"><b class="metric {"rank1" if i==0 else ""}">{i+1:02}</b>　<b>{x["name"]}</b> <span class="tag">{x["style"]}</span><span style="float:right">{x["total"]:.3f}s　| BEST {x["fast"]:.3f}　| {x["top"]:.0f} km/h　| AVG {x["avg"]:.0f}</span></div>',unsafe_allow_html=True)

def similarity(a,b,keys):return max(0,round(100-math.sqrt(sum((a[k]-b[k])**2 for k in keys)/len(keys))*1.25))
def match():
 s=calc();keys=['top_speed','downforce','grip','stability','cornering','tire_wear'];scores={n:similarity(s,v,keys) for n,v in TEAMS.items()};best=max(scores,key=scores.get)
 st.title('TEAM MATCH // DESIGN DNA');a,b=st.columns([1,1])
 with a:st.markdown('<div class="panel">'+car_svg(s)+'<h3>YOUR CAR PROFILE</h3></div>',unsafe_allow_html=True);gauges(s,keys)
 with b:
  st.markdown(f'<div class="panel"><div class="eyebrow">CLOSEST DESIGN PHILOSOPHY</div><div class="logo">{best.upper()}</div><div class="metric red">{scores[best]}% MATCH</div><p>※ 실제 시즌 성능이 아닌, 게임에서 정의한 가상의 팀 성향입니다.</p></div>',unsafe_allow_html=True)
  diffs=sorted(keys,key=lambda k:abs(s[k]-TEAMS[best][k]))[:3]
  st.subheader('WHY?');
  for k in diffs:st.write(f"✓ {LABELS[k]} 성향이 팀 기준과 유사합니다 ({s[k]} vs {TEAMS[best][k]})")
  for n,v in sorted(scores.items(),key=lambda x:-x[1]):st.progress(v/100,text=f'{n} — {v}%')

QUEST=[('레이스에서 가장 중요한 것은?',[('압도적인 최고속도','speed'),('완벽한 코너링','precision'),('안정적인 주행','stability'),('과감한 전략','strategy')]),('추월 기회가 보이면?',[('즉시 공격','risk'),('데이터를 확인','precision'),('실수를 기다림','strategy'),('안전하게 유지','stability')]),('새 규정이 도입됐다.',[('극단적 혁신','innovation'),('검증된 해법','stability'),('시뮬레이션 집중','precision'),('허점을 전략화','strategy')]),('당신의 피트월 스타일은?',[('직감적','risk'),('계산적','strategy'),('침착함','stability'),('실험적','innovation')]),('예선 마지막 랩이라면?',[('한계를 넘는다','risk'),('정확하게 완주','precision'),('직선 셋업','speed'),('새 라인을 시도','innovation')]),('타이어가 떨어질 때?',[('계속 밀어붙임','risk'),('페이스 관리','stability'),('언더컷 시도','strategy'),('주행법 수정','innovation')]),('가장 멋진 승리는?',[('최고속도 압도','speed'),('0.001초 차','precision'),('전략 역전','strategy'),('신기술 데뷔승','innovation')]),('팀 동료와 경쟁하면?',[('정면 승부','risk'),('데이터 공유','stability'),('약점을 분석','strategy'),('내 방식 개발','innovation')])]
def psychology():
 st.title('TEAM PSYCHOLOGY // DRIVER IDENTITY');st.caption('차량 설계 분석과 독립적인 8문항 성향 테스트입니다.')
 answers={};
 with st.form('psyform'):
  for i,(q,opts) in enumerate(QUEST):answers[i]=st.radio(f'{i+1:02}. {q}',[x[0] for x in opts],horizontal=True,key=f'q{i}')
  go=st.form_submit_button('ANALYZE PERSONALITY',use_container_width=True)
 if go:
  raw={k:30 for k in ['speed','risk','stability','strategy','innovation','precision']}
  for i,(_,opts) in enumerate(QUEST):raw[next(k for text,k in opts if text==answers[i])]+=18
  profile={k:min(99,v) for k,v in raw.items()};scores={n:similarity(profile,v,list(profile)) for n,v in PSY_TEAMS.items()};best=max(scores,key=scores.get)
  st.session_state.psy=(profile,best,scores[best])
 if 'psy' in st.session_state:
  p,b,sc=st.session_state.psy;a,c=st.columns(2)
  with a:
   st.subheader('YOUR RACING PERSONALITY')
   for k,v in p.items():st.progress(v/100,text=f'{k.upper()} — {v}')
  with c:st.markdown(f'<div class="panel"><div class="eyebrow">YOUR TEAM MATCH</div><div class="logo">{b.upper()}</div><div class="metric red">{sc}%</div><p>당신은 {"정교한 전략과 안정적 운영" if p["strategy"]+p["stability"]>p["risk"]+p["speed"] else "속도와 과감한 도전"}을 중요하게 생각하는 드라이버입니다.</p></div>',unsafe_allow_html=True)

nav();
try:
 {"HOME":home,"TUTORIAL":tutorial,"GARAGE":garage,"TEST":testlab,"RACE":race,"MATCH":match,"PSY":psychology}.get(st.session_state.page,home)()
except Exception as e:
 st.error('Race Control이 일시적인 오류를 감지했습니다. HOME으로 복귀해 주세요.');st.caption(str(e))
st.markdown('<hr><div class="small muted">APEX FORGE © ORIGINAL FICTIONAL MOTORSPORT EXPERIENCE · 실제 F1 차량/팀/로고와 무관합니다.</div>',unsafe_allow_html=True)
