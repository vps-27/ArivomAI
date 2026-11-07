import os
import base64
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

API_KEY = os.getenv("GNANI_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
ASSETS = Path(__file__).parent / "assets"

print("Environment file found:", ENV_PATH.exists())
print("API key loaded:", bool(API_KEY))
print("API key length:", len(API_KEY))

st.set_page_config(
    page_title="Arivom AI | அறிவோம் AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def b64(name):
    p = ASSETS / name
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""


HERO, LOGO_BIG, LOGO_SM, HOUSE = (
    b64("hero.jpg"), b64("logo_big.png"), b64("logo_small.png"), b64("house.png")
)

MISSING = [
    n for n in ["hero.jpg", "logo_big.png", "logo_small.png", "house.png"]
    if not (ASSETS / n).exists()
]
if MISSING:
    st.warning(f"Missing in {ASSETS.resolve()}: {', '.join(MISSING)}")

# ───────────────────────── IMAGE CSS ─────────────────────────
def _bg(cls, data, mime):
    if not data:
        return ""
    return f".{cls}{{background-image:url(data:{mime};base64,{data})}}\n"


IMG_CSS = (
    _bg("sb-logo", LOGO_SM, "image/png")
    + _bg("sb-house", HOUSE, "image/png")
    + _bg("logobig", LOGO_BIG, "image/png")
    + _bg("hero2-img", HERO, "image/jpeg")
)
st.markdown(f"<style>{IMG_CSS}</style>", unsafe_allow_html=True)


# ───────────────────────── STYLE ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

:root{
  --emerald-900:#0c3f30; --emerald-800:#11513f; --emerald-700:#1a6650; --emerald-500:#3f8f6a; --emerald-200:#cfe6d8;
  --gold-400:#e9bf5a; --gold-200:#f6e3a6;
  --ink:#1f2d26; --ink-soft:#44564c; --muted:#6a7b71;
  --line:rgba(31,45,38,.08);
  --glass:rgba(255,255,255,.72);
  --shadow-lg:0 30px 60px -30px rgba(18,60,45,.45);
  --shadow-md:0 16px 34px -22px rgba(18,60,45,.38);
}

html,body,[class*="css"]{font-family:'Manrope','Noto Sans Tamil',sans-serif;color:var(--ink)}
#MainMenu,footer{visibility:hidden}
header[data-testid="stHeader"]{background:transparent!important}

/* layered page background */
.stApp{
  background:
    radial-gradient(1200px 500px at 85% -10%, rgba(233,191,90,.18), transparent 60%),
    radial-gradient(900px 500px at -10% 110%, rgba(63,143,106,.22), transparent 60%),
    linear-gradient(160deg,#faf6ec 0%,#f3f5e9 55%,#e9f2e3 100%);
}
.block-container{max-width:1240px;padding:1.4rem 2.2rem 3rem;position:relative;z-index:1}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"]{
  background:linear-gradient(185deg,#fdfaf3 0%,#f7f0de 100%);
  border-right:1px solid #eadfc8;
  box-shadow:10px 0 40px -28px rgba(70,55,20,.45);
}
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"]{display:none}
section[data-testid="stSidebar"] .block-container{padding-top:1.2rem}

.sb-brand{text-align:center;padding:4px 0 6px}
.sb-logo{width:84px;height:84px;margin:0 auto;background-repeat:no-repeat;background-position:center;background-size:contain;
  filter:drop-shadow(0 10px 14px rgba(12,63,48,.25));animation:floaty 6s ease-in-out infinite}
.sb-brand .t1{font-size:27px;font-weight:800;color:var(--emerald-900);line-height:1.1;margin-top:6px;letter-spacing:-.4px}
.sb-brand .t2{font-size:18px;font-weight:700;color:var(--emerald-700);margin-top:2px}
.sb-tag{display:inline-block;margin-top:10px;padding:5px 12px;border-radius:999px;background:rgba(233,191,90,.22);
  color:#7a5a12;font-size:11.5px;font-weight:800;letter-spacing:.5px}

section[data-testid="stSidebar"] .stButton>button{
  justify-content:flex-start;text-align:left;border-radius:16px;min-height:50px;padding:0 16px;
  font-weight:700;font-size:14.5px;color:var(--ink-soft);background:transparent;border:1px solid transparent;
  box-shadow:none;transition:all .25s ease}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(63,143,106,.10);color:var(--emerald-900);border-color:rgba(63,143,106,.18);transform:translateX(3px)}
section[data-testid="stSidebar"] .stButton>button[kind="primary"],
section[data-testid="stSidebar"] .stButton>button[data-testid="stBaseButton-primary"]{
  background:linear-gradient(120deg,#1f7556,#2f8a66);color:#fff;border-color:transparent;
  box-shadow:0 14px 24px -14px rgba(20,100,70,.9)}
section[data-testid="stSidebar"] .stButton>button p{font-size:14.5px;line-height:1.3}

.sb-line{border:none;border-top:1px solid #e7dcc4;margin:18px 6px 14px}
.sb-card{margin:0 6px;padding:14px 16px;border-radius:18px;background:linear-gradient(135deg,#0f4d3b,#1f7556);color:#f4f9f6;
  box-shadow:0 18px 30px -18px rgba(12,63,48,.8)}
.sb-card b{display:block;font-size:13px;letter-spacing:.3px;opacity:.85}
.sb-card span{display:block;font-size:20px;font-weight:800;margin-top:4px}
.st-key-sbfoot{margin-top:auto}
.sb-house{height:150px;background-repeat:no-repeat;background-position:center bottom;background-size:contain;opacity:.95;margin-top:12px}

/* ---------- hero ---------- */
.hero2{position:relative;overflow:hidden;border-radius:32px;min-height:420px;
  background:linear-gradient(120deg,#fbf7ec 0%,#f4f1e1 60%,#eef1df 100%);
  box-shadow:var(--shadow-lg);border:1px solid rgba(255,255,255,.7)}
.hero2::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;
  background:linear-gradient(90deg,rgba(251,247,236,1) 0%,rgba(251,247,236,.6) 38%,rgba(251,247,236,0) 62%)}
.hero2-img{position:absolute;right:0;top:0;bottom:0;width:66%;background-size:cover;background-position:left center;background-repeat:no-repeat;z-index:1;
  -webkit-mask-image:linear-gradient(to right,transparent 0%,#000 30%);mask-image:linear-gradient(to right,transparent 0%,#000 30%)}
.orb{position:absolute;border-radius:50%;filter:blur(42px);pointer-events:none;z-index:0;animation:drift 9s ease-in-out infinite}
.orb.o1{width:240px;height:240px;background:rgba(233,191,90,.35);left:-70px;top:-70px}
.orb.o2{width:200px;height:200px;background:rgba(63,143,106,.22);left:300px;bottom:-80px;animation-delay:-4s}
.dots{position:absolute;width:160px;height:120px;right:36px;top:36px;opacity:.55;z-index:0;
  background-image:radial-gradient(rgba(31,117,86,.4) 1.5px,transparent 1.5px);background-size:14px 14px}
.hero2-top{position:absolute;right:24px;top:18px;z-index:4;display:flex;gap:12px}
.pill{background:rgba(255,255,255,.9);border-radius:999px;padding:11px 18px;font-weight:700;font-size:14px;color:var(--ink);
  box-shadow:0 10px 22px -14px rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.9);position:relative;backdrop-filter:blur(6px)}
.pill .rd{position:absolute;top:8px;right:11px;width:9px;height:9px;border-radius:50%;background:#e5484d;box-shadow:0 0 0 3px #fff}
.hero2-body{position:relative;z-index:3;padding:44px 44px 28px 60px;max-width:64%}
.kicker{display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:999px;background:rgba(15,77,59,.08);
  color:var(--emerald-800);font-size:12.5px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;
  animation:kpulse 2.4s ease-in-out infinite}
.kicker i{width:7px;height:7px;border-radius:50%;background:var(--gold-400);box-shadow:0 0 0 4px rgba(233,191,90,.25)}
.brandrow{display:flex;align-items:center;gap:16px;margin-top:14px}
.logobig{width:86px;height:86px;flex:0 0 86px;background-repeat:no-repeat;background-position:center;background-size:contain;
  animation:glow 3s ease-in-out infinite}
.brandtxt{font-size:44px;font-weight:800;line-height:1.05;letter-spacing:-.8px;
  background:linear-gradient(100deg,#0c3f30 0%,#1f7556 40%,#c99a2e 70%,#0c3f30 100%);background-size:200% auto;
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:shine 5s linear infinite}
.brandtxt div:nth-child(2){font-size:34px;letter-spacing:0}
.tagline{margin-top:14px}
.tagline span{display:inline-block;padding:9px 20px;font-size:15.5px;font-weight:700;line-height:1.5;color:#3c3a16;
  background:linear-gradient(100deg,rgba(241,222,160,.2),rgba(233,191,90,.55) 12%,rgba(233,191,90,.55) 88%,rgba(241,222,160,.2));
  border-radius:38% 10% 42% 12%/34% 40% 30% 40%;box-shadow:0 14px 30px -20px rgba(160,120,20,.7)}
.uline{width:220px;height:4px;margin:12px 0 0 0;border-radius:99px;
  background:linear-gradient(90deg,#e9bf5a,#1f7556,#e9bf5a);background-size:200% auto;animation:shine 3s linear infinite}
.feats{display:flex;align-items:center;margin-top:26px;flex-wrap:wrap;gap:6px}
.feat{display:flex;align-items:center;gap:12px;padding:10px 22px 10px 18px;margin-right:6px;border-radius:18px;
  background:rgba(255,255,255,.7);border:1px solid rgba(255,255,255,.9);box-shadow:0 10px 22px -18px rgba(12,63,48,.6);
  font-weight:700;font-size:15px;line-height:1.35;color:var(--ink)}
.feat svg{flex:0 0 30px}
.trust{display:flex;align-items:center;flex-wrap:wrap;gap:10px;margin-top:22px;font-size:13px;font-weight:700;color:var(--emerald-700)}
.trust i{width:5px;height:5px;border-radius:50%;background:var(--gold-400)}
.status-chip{display:inline-flex;align-items:center;gap:10px;margin-top:18px;padding:9px 18px;border-radius:999px;
  background:linear-gradient(120deg,#0f4d3b,#2a7d5d);color:#fff;font-weight:800;font-size:14px;
  box-shadow:0 14px 26px -14px rgba(15,77,59,.9)}
.status-chip .live{width:9px;height:9px;border-radius:50%;background:#7ef0b5;animation:ping 1.8s infinite}
.float-card{position:absolute;z-index:5;background:rgba(255,255,255,.9);backdrop-filter:blur(8px);
  border:1px solid rgba(255,255,255,.95);border-radius:18px;padding:12px 16px;display:flex;gap:12px;align-items:center;
  box-shadow:0 18px 30px -20px rgba(12,63,48,.6);font-size:14px;font-weight:700;color:var(--ink);animation:drift 7s ease-in-out infinite}
.float-card small{display:block;font-weight:600;color:var(--muted);font-size:12px;margin-top:2px}
.float-card .fi{width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:18px;flex:0 0 40px}
.fi-red{background:linear-gradient(135deg,#fde0d6,#f7c3b0)}
.fi-green{background:linear-gradient(135deg,#d4eddf,#b6dcc7)}
.fc-bot{right:34px;bottom:34px;animation-delay:-3s}
@keyframes drift{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes shine{to{background-position:200% center}}
@keyframes kpulse{0%,100%{box-shadow:0 0 0 0 rgba(233,191,90,.45)}50%{box-shadow:0 0 0 8px rgba(233,191,90,0)}}
@keyframes glow{
  0%,100%{filter:drop-shadow(0 0 0 rgba(233,191,90,0)) drop-shadow(0 10px 14px rgba(12,63,48,.25))}
  50%{filter:drop-shadow(0 0 22px rgba(233,191,90,.8)) drop-shadow(0 10px 14px rgba(12,63,48,.25))}}
@keyframes ping{0%{box-shadow:0 0 0 0 rgba(126,240,181,.8)}70%,100%{box-shadow:0 0 0 10px rgba(126,240,181,0)}}
@media(max-width:1000px){
  .hero2-body{max-width:100%;padding:30px 24px}
  .hero2-img{width:100%;opacity:.25}
  .brandtxt{font-size:32px}
  .brandtxt div:nth-child(2){font-size:26px}
  .logobig{width:64px;height:64px;flex:0 0 64px}
  .float-card{display:none}
}

/* ---------- action cards ---------- */
.st-key-cardrow{margin-top:26px;position:relative;z-index:6}
.st-key-card_aw,.st-key-card_dr,.st-key-card_gd{position:relative;overflow:hidden;border-radius:26px;padding:24px 26px 26px!important;
  min-height:250px;border:1px solid rgba(255,255,255,.8);box-shadow:var(--shadow-md);transition:transform .35s ease,box-shadow .35s ease}
.st-key-card_aw:hover,.st-key-card_dr:hover,.st-key-card_gd:hover{transform:translateY(-6px);box-shadow:0 32px 56px -28px rgba(18,60,45,.55)}
.st-key-card_aw>*,.st-key-card_dr>*,.st-key-card_gd>*{position:relative;z-index:1}
.st-key-card_aw::after,.st-key-card_dr::after,.st-key-card_gd::after{content:"";position:absolute;left:0;right:0;top:0;height:4px;z-index:2}
.st-key-card_aw::after{background:linear-gradient(90deg,#1f7556,#6cc49a)}
.st-key-card_dr::after{background:linear-gradient(90deg,#b83a2e,#ef8f6b)}
.st-key-card_gd::after{background:linear-gradient(90deg,#1d4e89,#6ea6e6)}
.st-key-card_aw::before,.st-key-card_dr::before,.st-key-card_gd::before{content:"";position:absolute;right:-10px;bottom:-10px;width:150px;height:150px;
  background:no-repeat center/contain;opacity:.10;pointer-events:none;z-index:0}
.st-key-card_aw::before{background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231f7556' stroke-width='1.1'><path d='M3 5h14v10H8l-5 4z'/><path d='M7 9h6M7 12h4' /></svg>")}
.st-key-card_dr::before{background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23b83a2e' stroke-width='0.9'><path d='M0 12h3l2-7 3 14 3-11 2 6 2-2h6'/></svg>")}
.st-key-card_gd::before{background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231d4e89' stroke-width='0.9'><path d='M1 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H1zM23 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z'/></svg>")}
.st-key-card_aw{background:linear-gradient(160deg,#ffffff 0%,#eef7f1 60%,#dff0e6 100%)}
.st-key-card_dr{background:linear-gradient(160deg,#ffffff 0%,#fff6ee 60%,#fde7d6 100%)}
.st-key-card_gd{background:linear-gradient(160deg,#ffffff 0%,#f1f6fd 60%,#dfeafa 100%)}
.chead{display:flex;align-items:center;gap:16px;margin-bottom:12px}
.cic{width:60px;height:60px;border-radius:18px;display:flex;align-items:center;justify-content:center;flex:0 0 60px;
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.8),0 12px 22px -14px rgba(0,0,0,.35)}
.cic svg{width:30px;height:30px}
.ic-g{background:linear-gradient(135deg,#d4eddf,#b6dcc7)}
.ic-r{background:linear-gradient(135deg,#fde0d6,#f7c3b0)}
.ic-b{background:linear-gradient(135deg,#d9e7fb,#b9d3f3)}
.ctitle{font-size:21px;font-weight:800;line-height:1.25;color:var(--ink)}
.cdesc{font-size:14.5px;line-height:1.7;color:var(--ink-soft);margin-bottom:14px;min-height:72px}
.st-key-card_aw .stButton>button,.st-key-card_dr .stButton>button,.st-key-card_gd .stButton>button{width:auto;border-radius:999px;min-height:46px;padding:0 24px;color:#fff;font-weight:700;border:none;box-shadow:0 14px 24px -14px rgba(0,0,0,.55);transition:all .25s ease}
.st-key-card_aw .stButton>button{background:linear-gradient(120deg,#1f7556,#2f8a66)}
.st-key-card_dr .stButton>button{background:linear-gradient(120deg,#a8342a,#c9503f)}
.st-key-card_gd .stButton>button{background:linear-gradient(120deg,#1d4e89,#2f6cb3)}
.st-key-card_aw .stButton>button:hover,.st-key-card_dr .stButton>button:hover,.st-key-card_gd .stButton>button:hover{filter:brightness(1.1);color:#fff;transform:translateY(-2px)}

/* ---------- bottom row ---------- */
.remember{background:linear-gradient(145deg,rgba(255,255,255,.85),rgba(236,245,234,.9));border:1px solid rgba(255,255,255,.9);
  border-radius:26px;padding:22px 28px;box-shadow:var(--shadow-md)}
.remember h4{margin:0 0 14px;font-size:20px;font-weight:800;color:var(--ink)}
.rem-row{display:flex}
.rem{flex:1;display:flex;gap:14px;align-items:center;padding:0 18px;border-right:1.5px solid #d6e0cc;font-size:14.5px;line-height:1.55;font-weight:600;color:var(--ink)}
.rem:first-child{padding-left:0}.rem:last-child{border-right:none}
.rem svg{flex:0 0 32px;width:32px;height:32px}
.sos2{background:linear-gradient(160deg,#ffffff,#f6fbf8);border:1px solid rgba(255,255,255,.9);border-radius:26px;padding:20px 22px;text-align:center;box-shadow:var(--shadow-md);color:var(--ink)}
.sos2 .top{display:flex;gap:10px;align-items:center;justify-content:center;font-weight:800;font-size:16.5px}
.sos2 .num{display:inline-block;margin:12px 0 6px;padding:9px 34px;border-radius:999px;background:linear-gradient(120deg,#0f4d3b,#2a7d5d);color:#fff;font-size:30px;font-weight:800;letter-spacing:1px;box-shadow:0 14px 24px -12px rgba(15,77,59,.9)}
.sos2 small{display:block;color:var(--muted);font-weight:600}
@media(max-width:1000px){.rem-row{flex-direction:column;gap:12px}.rem{border:none;padding:0}}

/* ---------- inner pages ---------- */
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;gap:16px}
.topbar .eyebrow{font-size:12px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#b07d1c}
.topbar h2{margin:4px 0 0;font-size:32px;font-weight:800;color:var(--emerald-900);letter-spacing:-.4px}
.topbar p{margin:6px 0 0;color:var(--muted);font-size:14.5px;max-width:640px;line-height:1.6}
.topbar .pills{display:flex;gap:10px;flex-shrink:0}

[class*="st-key-panel"]{background:var(--glass);border:1px solid rgba(255,255,255,.9);border-radius:28px;padding:26px 28px!important;
  box-shadow:var(--shadow-lg);backdrop-filter:blur(10px)}
.stTextInput input{border-radius:16px!important;border:1.5px solid #d6e0cf!important;padding:14px 18px!important;background:#fff!important;font-size:15px!important;color:var(--ink)!important}
.stTextInput input::placeholder {
    color: #6a7b71 !important;
    opacity: 1 !important;
}
.stTextInput input:focus{border-color:#2f8a66!important;box-shadow:0 0 0 4px rgba(47,138,102,.15)!important}
.stTextInput label,.stAudioInput label,.stSelectbox label,.stSelectbox p{font-weight:700!important;color:var(--emerald-900)!important}
div[data-baseweb="select"]>div{border-radius:16px!important;border:1.5px solid #d6e0cf!important;min-height:50px;background:#fff!important}
[data-testid="stAudioInput"]{border-radius:20px;border:1.5px dashed #9cc9b1;background:linear-gradient(135deg,#f5fbf7,#eaf5ee);padding:8px}
[class*="st-key-panel"] .stButton>button,.st-key-prog .stButton>button{border-radius:999px;min-height:50px;font-weight:700;color:#fff;border:none;
  background:linear-gradient(120deg,#0f4d3b,#2a7d5d);box-shadow:0 16px 26px -14px rgba(15,77,59,.9);transition:all .25s ease}
[class*="st-key-panel"] .stButton>button:hover{transform:translateY(-2px);filter:brightness(1.1);color:#fff}

.answer{background:linear-gradient(160deg,#ffffff,#f2faf5);border:1px solid #cfe6d8;border-left:5px solid #2f8a66;border-radius:22px;
  padding:22px 24px;box-shadow:var(--shadow-md);margin-top:8px}
.answer small{font-weight:800;color:var(--emerald-700);letter-spacing:.7px;font-size:11.5px;text-transform:uppercase}
.answer p{margin:8px 0 0;font-size:16.5px;line-height:1.8;color:var(--ink)}
.recog{background:#eef6fb;border:1px solid #d3e6f2;border-radius:16px;padding:12px 16px;font-size:14px;margin:12px 0;color:var(--ink)}

.bubble{display:flex;gap:12px;margin:16px 0;align-items:flex-end}
.avatar{flex:0 0 46px;height:46px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 10px 18px -12px rgba(0,0,0,.4)}
.av-bad{background:linear-gradient(135deg,#ffd9d4,#ffb8ab)}
.av-ok{background:linear-gradient(135deg,#d4f2e2,#a9dfc4)}
.msg{border-radius:20px;padding:15px 19px;line-height:1.75;font-size:15.5px;max-width:86%;color:var(--ink);box-shadow:0 12px 24px -18px rgba(0,0,0,.35)}
.msg small{display:block;font-weight:800;font-size:11.5px;letter-spacing:.6px;text-transform:uppercase;margin-bottom:4px}
.msg.bad{background:linear-gradient(160deg,#fff7f5,#fff0ec);border:1px solid #ffd2cc;border-bottom-left-radius:6px}
.msg.bad small{color:#b83a2e}
.msg.ok{background:linear-gradient(160deg,#f2fbf6,#e5f7ec);border:1px solid #bfe6cf;border-bottom-left-radius:6px}
.msg.ok small{color:var(--emerald-700)}

.verdict{border-radius:22px;padding:20px 24px;margin:14px 0;display:flex;gap:16px;align-items:flex-start;box-shadow:var(--shadow-md)}
.verdict.good{background:linear-gradient(135deg,#effcf4,#dcf3e6);border:1px solid #a9e3c5}
.verdict.try{background:linear-gradient(135deg,#fff9ee,#fff0d4);border:1px solid #f4d59a}
.verdict .vi{font-size:30px;line-height:1}
.verdict h4{margin:0 0 6px;font-size:17px;font-weight:800}
.verdict.good h4{color:var(--emerald-700)}.verdict.try h4{color:#b35d05}
.verdict p{margin:0;font-size:15px;line-height:1.7;color:var(--ink)}

.chip{display:inline-block;padding:6px 14px;border-radius:999px;font-size:12px;font-weight:800;background:#e3efe6;color:var(--emerald-900);border:1px solid #c9dfd0}
.chip.hot{background:#fff1e0;color:#a4530a;border-color:#f7d9ac}

.score{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:16px 0}
.stat{background:linear-gradient(160deg,#ffffff,#f4faf6);border:1px solid rgba(255,255,255,.9);border-radius:22px;padding:20px 22px;box-shadow:var(--shadow-md);color:var(--ink);display:flex;align-items:center;gap:16px}
.stat b{display:block;font-size:30px;font-weight:800;color:var(--emerald-900);line-height:1}
.stat span{font-size:13px;color:var(--muted);font-weight:600;display:block;margin-top:6px}
.ring{width:72px;height:72px;border-radius:50%;flex:0 0 72px;display:flex;align-items:center;justify-content:center;position:relative}
.ring::after{content:"";position:absolute;inset:9px;border-radius:50%;background:#fff}
.ring b{position:relative;z-index:1;font-size:15px!important;margin:0!important}
.bdg{padding:12px 18px;border-radius:16px;background:#fff;border:1px solid #e3e8da;font-weight:700;font-size:14px;color:var(--ink);box-shadow:0 8px 16px -14px rgba(0,0,0,.4)}
.bdg.on{background:linear-gradient(135deg,#effcf4,#dcf3e6);border-color:#a9e3c5;color:var(--emerald-700)}
.bdg.off{opacity:.45;filter:grayscale(1)}
.badges2{display:flex;gap:12px;flex-wrap:wrap;margin-top:8px}

div[data-testid="stExpander"]{border:1px solid rgba(255,255,255,.9)!important;border-radius:18px!important;background:rgba(255,255,255,.85);margin-bottom:12px;overflow:hidden;box-shadow:0 10px 22px -18px rgba(0,0,0,.35)}
div[data-testid="stExpander"] summary{font-weight:700;padding:8px 10px}
div[data-testid="stAlert"]{border-radius:16px}

.grass{position:fixed;left:262px;right:0;bottom:0;height:160px;pointer-events:none;z-index:0;
  background:linear-gradient(to top,#8fb36a 0%,#b7d196 45%,rgba(200,224,170,0) 100%)}
.foot{text-align:center;color:var(--muted);font-size:12.5px;padding:26px 0 0;position:relative;z-index:1}
@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}

/* ---- back to home ---- */
.st-key-backrow{margin-bottom:6px}
.st-key-backrow .stButton>button{
  border-radius:999px;min-height:42px;padding:0 20px;font-weight:700;font-size:14px;
  color:var(--emerald-900);background:#fff;border:1.5px solid #cfe6d8;
  box-shadow:0 10px 20px -16px rgba(12,63,48,.6);transition:all .25s ease
}
.st-key-backrow .stButton>button:hover{
  background:#eef7f1;border-color:#2f8a66;transform:translateX(-3px)
}
/* ---- expander text visibility ---- */
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] li,
div[data-testid="stExpander"] details div{
  color:var(--ink)!important;
  opacity:1!important;
}
div[data-testid="stExpander"] summary svg{fill:var(--emerald-700)!important;color:var(--emerald-700)!important}
div[data-testid="stExpander"]{background:#ffffff!important}
</style>
""", unsafe_allow_html=True)

# ───────────────────────── LINE ICONS (inline SVG) ─────────────────────────
def svg(paths, color="#1f7556", size=30, sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')


ICON_MIC = '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>'
ICON_HEADSET = '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>'
ICON_SHIELD = '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>'
ICON_CHAT = '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/>'
ICON_PHONE = '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>'
ICON_BOOK = '<path d="M2 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2zM22 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/>'
ICON_LOCK = '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'
ICON_LINK = '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>'
ICON_FAMILY = '<circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M2 20a6 6 0 0 1 12 0M12 20a6 6 0 0 1 10 0"/>'


# ───────────────────────── GNANI API ─────────────────────────
def prisma(audio_bytes):
    if not API_KEY:
        raise ValueError("GNANI_API_KEY is missing in .env")

    r = requests.post(
        "https://api.vachana.ai/stt/v3",
        headers={"X-API-Key-ID": API_KEY},
        data={"model": "prisma-v3.0", "language_code": "ta-IN"},
        files={"audio_file": ("response.wav", audio_bytes, "audio/wav")},
        timeout=60
    )

    if r.status_code != 200:
        print("Gnani STT status:", r.status_code)
        print("Gnani STT response:", r.text)
        raise RuntimeError(f"Gnani STT failed ({r.status_code}): {r.text}")

    return r.json().get("transcript", "").strip()


def timbre(text):
    if not API_KEY:
        raise ValueError("GNANI_API_KEY is missing in .env")

    r = requests.post(
        "https://api.vachana.ai/api/v1/tts/inference",
        headers={"X-API-Key-ID": API_KEY, "Content-Type": "application/json"},
        json={
            "text": text,
            "model": "timbre-v2.5",
            "voice": "Brinda",
            "language": "ta-IN",
            "speed": 1.0,
            "audio_config": {
                "encoding": "linear_pcm",
                "container": "wav",
                "num_channels": 1,
                "sample_rate": 48000,
                "sample_width": 2
            }
        },
        timeout=90
    )

    if r.status_code != 200:
        print("Gnani TTS status:", r.status_code)
        print("Gnani TTS response:", r.text)
        raise RuntimeError(f"Gnani TTS failed ({r.status_code}): {r.text}")

    return r.content


# ───────────────────────── CONTENT ─────────────────────────
SCENARIOS = [
    {
        "title": "வங்கி OTP மோசடி",
        "level": "Beginner",
        "line": "வணக்கம் ஐயா, நான் உங்கள் வங்கியிலிருந்து பேசுகிறேன். உங்கள் கணக்கை சரிபார்க்க OTP எண்ணை உடனே சொல்லுங்கள்.",
        "safe": ["பகிரமாட்ட", "சொல்லமாட்ட", "தரமாட்ட", "பகிர முடியாது", "அழைப்பை துண்ட", "வங்கியை நானே தொடர்பு"],
        "unsafe": ["otp இதோ", "ஓடிபி இதோ", "சொல்கிறேன்", "பகிர்கிறேன்", "கொடுக்கிறேன்"],
        "good": "சரியான பதில். OTP-ஐ யாரிடமும் பகிர வேண்டாம். அழைப்பைத் துண்டித்து, வங்கியின் அதிகாரப்பூர்வ எண்ணை நீங்களே தொடர்புகொள்ளுங்கள்.",
        "bad": "OTP-ஐ தொலைபேசியில் யாரிடமும் பகிரக்கூடாது. வங்கி ஊழியர் என்று கூறினாலும் OTP, PIN அல்லது CVV கேட்பது மோசடியின் அறிகுறி.",
        "hint": "OTP பகிர மறுத்து அழைப்பைத் துண்டிக்கவும்; வங்கியை அதிகாரப்பூர்வ வழியில் தொடர்புகொள்ளவும்."
    },
    {
        "title": "UPI பணம் பெறும் மோசடி",
        "level": "Intermediate",
        "line": "உங்களுக்கு பணம் அனுப்பியுள்ளோம். பணத்தைப் பெற இந்த UPI collect request-ஐ approve செய்து உங்கள் PIN-ஐ உள்ளிடுங்கள்.",
        "safe": ["நிராகரி", "மறுக்க", "pin உள்ளிடமாட்ட", "பின் உள்ளிடமாட்ட", "approve செய்யமாட்ட", "பணம் பெற pin தேவையில்லை"],
        "unsafe": ["approve செய்கிறேன்", "pin உள்ளிடுகிறேன்", "பின் எண்ணை தருகிறேன்", "அனுமதி தருகிறேன்"],
        "good": "நல்ல முடிவு. பணம் பெறுவதற்கு UPI PIN தேவையில்லை. தெரியாத collect request-ஐ நிராகரிக்கவும்.",
        "bad": "UPI PIN பணம் செலுத்துவதற்காக மட்டுமே. பணம் பெற PIN தேவையில்லை. தெரியாத collect request-ஐ approve செய்ய வேண்டாம்.",
        "hint": "தெரியாத UPI collect request-ஐ நிராகரிக்கவும்; PIN உள்ளிட வேண்டாம்."
    },
    {
        "title": "போலி வேலைவாய்ப்பு மோசடி",
        "level": "Intermediate",
        "line": "உங்களுக்கு பெரிய நிறுவனத்தில் வேலை உறுதி. உடனே registration fee அனுப்பினால் offer letter கிடைக்கும்.",
        "safe": ["பணம் அனுப்பமாட்ட", "கட்டணம் செலுத்தமாட்ட", "முதலில் சரிபார", "அதிகாரப்பூர்வ இணையதள", "மறுக்கிறேன்"],
        "unsafe": ["பணம் அனுப்புகிறேன்", "கட்டணம் செலுத்துகிறேன்", "upi மூலம் அனுப்புகிறேன்"],
        "good": "சரியான அணுகுமுறை. வேலை உறுதி செய்ய முன்பணம் கேட்பது மோசடி எச்சரிக்கை அறிகுறி. நிறுவனத்தின் அதிகாரப்பூர்வ career page-ல் சரிபார்க்கவும்.",
        "bad": "வேலை அல்லது offer letter பெற முன்பணம் செலுத்த வேண்டாம். நிறுவனத்தின் அதிகாரப்பூர்வ இணையதளம் மற்றும் தொடர்பு விவரங்களைச் சரிபார்க்கவும்.",
        "hint": "பணம் அனுப்ப மறுத்து, நிறுவனத்தின் அதிகாரப்பூர்வ career page-ல் சரிபார்க்கவும்."
    },
    {
        "title": "போலி SMS / phishing link",
        "level": "Beginner",
        "line": "உங்கள் வங்கி கணக்கு இன்று முடக்கப்படும். இந்த SMS link-ஐ திறந்து உங்கள் card மற்றும் login விவரங்களை update செய்யுங்கள்.",
        "safe": ["திறக்கமாட்ட", "கிளிக் செய்யமாட்ட", "வங்கியை தொடர்பு", "அதிகாரப்பூர்வ app", "சரிபார்க்கிறேன்"],
        "unsafe": ["link திறக்கிறேன்", "கிளிக் செய்கிறேன்", "விவரங்களை உள்ளிடுகிறேன்", "card விவரம் தருகிறேன்"],
        "good": "நன்றாகச் செய்தீர்கள். எதிர்பாராத SMS link-ஐ திறக்காதீர்கள். வங்கியின் அதிகாரப்பூர்வ app அல்லது website-ஐ நீங்களே திறந்து சரிபார்க்கவும்.",
        "bad": "இது phishing முயற்சியாக இருக்கலாம். SMS link-ஐ திறக்கவோ password, card அல்லது OTP விவரங்களை உள்ளிடவோ வேண்டாம்.",
        "hint": "SMS link-ஐ திறக்காமல் வங்கியின் அதிகாரப்பூர்வ app அல்லது website-ல் சரிபார்க்கவும்."
    }
]

FAQ = [
    (
        "OTP-ஐ யாரிடமாவது பகிரலாமா?",
        "இல்லை. OTP, PIN, CVV மற்றும் password போன்ற ரகசிய விவரங்களை யாரிடமும் பகிர வேண்டாம். வங்கி ஊழியர் என்று கூறுபவர்களிடமும் பகிர வேண்டாம்.",
        ["otp", "ஓடிபி", "cvv", "password", "பாஸ்வேர்ட்"]
    ),
    (
        "பணம் பெற UPI PIN உள்ளிட வேண்டுமா?",
        "இல்லை. UPI PIN பணம் செலுத்தும்போது மட்டுமே பயன்படுத்தப்படுகிறது. பணம் பெறுவதற்கு PIN தேவையில்லை. தெரியாத collect request-ஐ நிராகரிக்கவும்.",
        ["upi", "பணம் பெற", "collect request"]
    ),
    (
        "வேலைக்காக registration fee கேட்கிறார்கள். என்ன செய்யலாம்?",
        "முன்பணம் செலுத்த வேண்டாம். நிறுவனத்தின் அதிகாரப்பூர்வ career website மூலம் வேலைவாய்ப்பைச் சரிபார்க்கவும்.",
        ["வேலை", "job", "registration fee", "offer letter"]
    ),
    (
        "சந்தேகமான SMS link-ஐ திறக்கலாமா?",
        "எதிர்பாராத அல்லது சந்தேகமான link-ஐ திறக்க வேண்டாம். சம்பந்தப்பட்ட நிறுவனத்தின் அதிகாரப்பூர்வ app அல்லது website-ஐ நீங்களே திறந்து சரிபார்க்கவும்.",
        ["link", "லிங்க்", "sms", "phishing"]
    ),
    (
        "ஆன்லைன் பண மோசடி நடந்தால் என்ன செய்ய வேண்டும்?",
        "உடனடியாக உங்கள் வங்கியைத் தொடர்புகொண்டு கணக்கைப் பாதுகாக்கவும். இந்தியாவில் 1930 என்ற தேசிய சைபர் குற்ற உதவி எண்ணை அழைக்கவும் அல்லது cybercrime.gov.in-ல் புகார் அளிக்கவும்.",
        ["புகார்", "பணம் போய்விட்டது", "மோசடி நடந்த", "1930", "cybercrime"]
    )
]


def faq_answer(q):
    q = q.lower()
    ranked = [
        (sum(term in q for term in terms), ans)
        for question, ans, terms in FAQ
    ]
    score, ans = max(ranked, key=lambda x: x[0])
    return ans if score else "இந்தக் கேள்விக்கான உறுதிப்படுத்தப்பட்ட தகவல் என்னிடம் இல்லை. உங்கள் வங்கி அல்லது அதிகாரப்பூர்வ சைபர் குற்ற உதவி மையத்தை அணுகவும்."


def evaluate_fallback(s, reply):
    """Offline keyword fallback; not a semantic language model."""
    t = reply.lower().strip()

    if not t:
        return False, "பதிலைப் புரிந்துகொள்ள முடியவில்லை. மீண்டும் முயற்சிக்கவும்."

    if any(x in t for x in s["unsafe"]):
        return False, s["bad"]

    if any(x in t for x in s["safe"]):
        return True, s["good"]

    return False, "பாதுகாப்பான செயல் உங்கள் பதிலில் தெளிவாக இல்லை. " + s["hint"]


def evaluate(s, reply):
    """
    Use Gemini to judge the meaning of a Tamil/Tanglish answer.
    Returns (is_safe, Tamil feedback, evaluation_source).
    Falls back to the original keyword rules if Gemini is not configured
    or the API request fails.
    """
    answer = reply.strip()
    if not answer:
        return False, "பதிலைப் புரிந்துகொள்ள முடியவில்லை. மீண்டும் முயற்சிக்கவும்.", "empty"

    if not GEMINI_API_KEY:
        ok, feedback = evaluate_fallback(s, answer)
        return ok, feedback, "fallback"

    prompt = f"""
நீங்கள் Arivom AI என்ற தமிழ் டிஜிட்டல் மோசடி விழிப்புணர்வு பயிற்சியின் மதிப்பீட்டாளர்.

கீழே உள்ள சூழ்நிலைக்கு பயனர் அளித்த பதிலை அதன் பொருளைப் புரிந்து மதிப்பிடுங்கள்.
தமிழ், Tanglish, எழுத்துப் பிழைகள் மற்றும் இயல்பான பேச்சு வழக்கை புரிந்துகொள்ள முயலுங்கள்.

முக்கிய விதிகள்:
- பயனர் மோசடியை மறுத்து, OTP/PIN/CVV/password பகிராமல், சந்தேகமான request/link-ஐ நிராகரித்து, அதிகாரப்பூர்வ வழியில் சரிபார்ப்பதாகக் கூறினால் SAFE.
- பயனர் மோசடியாளரின் கோரிக்கையை ஏற்கிறார், ரகசிய விவரங்களைப் பகிர்கிறார், பணம் அனுப்புகிறார் அல்லது சந்தேகமான link-ல் விவரம் உள்ளிடுகிறார் என்றால் UNSAFE.
- பதில் தெளிவற்றதாகவோ, சூழ்நிலைக்கு பொருந்தாததாகவோ இருந்தால் UNCLEAR.
- ஒரு குறிப்பிட்ட முக்கியச் சொல்லை மட்டும் தேடி முடிவு செய்யாதீர்கள்; முழு வாக்கியத்தின் பொருளை மதிப்பிடுங்கள்.
- பயனர் பாதுகாப்பான செயலைத் தெளிவாகச் சொன்னால், கூடுதல் விளக்கம் இல்லாததற்காக தவறாக மதிப்பிடாதீர்கள்.
- பதிலில் இல்லாத தகவலைக் கற்பனை செய்யாதீர்கள்.
- இது பயிற்சி மட்டுமே; உண்மையான நிதி அல்லது பாதுகாப்பு முடிவாகக் கருத வேண்டாம்.

சூழ்நிலை: {s["title"]}
சந்தேகமான நபர் கூறியது: {s["line"]}
பாதுகாப்பான செயல்: {s["hint"]}
பயனரின் பதில்: {answer}

JSON வடிவில் மட்டும் பதிலளிக்கவும்:
{{
  "verdict": "SAFE" 또는 "UNSAFE" 또는 "UNCLEAR",
  "feedback_ta": "எளிய தமிழில் 1 முதல் 3 வாக்கியங்களில் காரணத்துடன் கருத்து"
}}
"""

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    try:
        response = requests.post(
            url,
            headers={
                "x-goog-api-key": GEMINI_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "responseMimeType": "application/json"
                }
            },
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Gemini API error ({response.status_code}): {response.text[:500]}"
            )

        payload = response.json()
        generated = payload["candidates"][0]["content"]["parts"][0]["text"]
        result = json.loads(generated)

        verdict = str(result.get("verdict", "UNCLEAR")).upper().strip()
        feedback = str(result.get("feedback_ta", "")).strip()

        if verdict not in {"SAFE", "UNSAFE", "UNCLEAR"} or not feedback:
            raise ValueError("Gemini returned an invalid evaluation format.")

        if verdict == "SAFE":
            return True, feedback, "gemini"
        if verdict == "UNSAFE":
            return False, feedback, "gemini"

        return False, feedback, "gemini"

    except Exception as exc:
        # Keep the drill usable if Gemini is unavailable.
        print("Gemini evaluation unavailable; using keyword fallback:", exc)
        ok, feedback = evaluate_fallback(s, answer)
        return ok, feedback + " (தற்காலிக keyword மதிப்பீடு)", "fallback"


# ───────────────────────── STATE & NAV ─────────────────────────
st.session_state.setdefault("page", "home")
st.session_state.setdefault("tries", 0)
st.session_state.setdefault("safe_count", 0)


def go(p):
    st.session_state["page"] = p


def back_home():
    with st.container(key="backrow"):
        st.button(
            "🏠 முகப்புக்குத் திரும்புங்கள்",
            key="back_home",
            on_click=go,
            args=("home",)
        )


NAV = [
    ("home", ":material/home:", "முகப்பு"),
    ("aw", ":material/chat_bubble:", "மோசடி விழிப்புணர்வு"),
    ("dr", ":material/call:", "Scam Drill (பயிற்சி முறை)"),
    ("gd", ":material/menu_book:", "பாதுகாப்பு வழிகாட்டி"),
    ("pg", ":material/bar_chart:", "என் முன்னேற்றம்"),
]

st.markdown('<div class="grass"></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        '<div class="sb-brand"><div class="sb-logo"></div><div class="t1">Arivom AI</div><div class="t2">அறிவோம் AI</div><span class="sb-tag">DIGITAL SAFETY</span></div>',
        unsafe_allow_html=True
    )

    for k, ic, lb in NAV:
        st.button(
            lb,
            key=f"nav_{k}",
            icon=ic,
            type="primary" if st.session_state["page"] == k else "secondary",
            on_click=go,
            args=(k,),
            use_container_width=True
        )

    st.markdown('<hr class="sb-line"/>', unsafe_allow_html=True)

    safe_pct = int(100 * st.session_state["safe_count"] / st.session_state["tries"]) if st.session_state["tries"] else 0
    st.markdown(
        f'<div class="sb-card"><b>உங்கள் பாதுகாப்பு மதிப்பெண்</b><span>{safe_pct}%</span></div>',
        unsafe_allow_html=True
    )

    with st.container(key="sbfoot"):
        st.markdown('<div class="sb-house"></div>', unsafe_allow_html=True)


def topbar(eyebrow, title, sub):
    st.markdown(
        f'<div class="topbar"><div><div class="eyebrow">{eyebrow}</div><h2>{title}</h2><p>{sub}</p></div><div class="pills"><span class="pill">🔔<i class="rd"></i></span><span class="pill">👤 வணக்கம், பயனர்! ⌄</span></div></div>',
        unsafe_allow_html=True
    )


page = st.session_state["page"]

if page != "home":
    back_home()


# ───────────────────────── HOME ─────────────────────────
if page == "home":

    hero = (
        '<div class="hero2">'
        '<div class="orb o1"></div><div class="orb o2"></div><div class="dots"></div>'
        '<div class="hero2-img"></div>'
        '<div class="hero2-top"><span class="pill">🔔<i class="rd"></i></span><span class="pill">👤 வணக்கம், பயனர்! ⌄</span></div>'
        '<div class="hero2-body">'
        '<span class="kicker"><i></i>Digital Safety · டிஜிட்டல் பாதுகாப்பு</span>'
        '<div class="brandrow"><div class="logobig"></div><div class="brandtxt"><div>Arivom AI</div><div>அறிவோம் AI</div></div></div>'
        '<div class="tagline"><span>டிஜிட்டல் மோசடிகளை அறிந்து,<br>உங்களை பாதுகாக்கும் தமிழ் தோழன்.</span></div>'
        '<div class="uline"></div>'
        '<div class="feats">'
        f'<div class="feat">{svg(ICON_MIC, size=30)}<div>தமிழில்<br>கேளுங்கள்</div></div>'
        f'<div class="feat">{svg(ICON_HEADSET, size=30)}<div>எளிய<br>விளக்கம் பெறுங்கள்</div></div>'
        f'<div class="feat">{svg(ICON_SHIELD, size=30)}<div>பாதுகாப்பாக<br>இருங்கள்</div></div>'
        '</div>'
        '<div class="trust"><span>4 பயிற்சி காட்சிகள்</span><i></i><span>தமிழ் குரல் உதவி</span><i></i><span>உடனடி வழிகாட்டுதல்</span></div>'
        '<div class="status-chip"><span class="live"></span>🛡️ பாதுகாப்பு நிலை</div>'
        '</div>'
        '<div class="float-card fc-bot"><div class="fi fi-red">📞</div><div>1930<small>தேசிய சைபர் குற்ற உதவி எண்</small></div></div>'
        '</div>'
    )
    st.markdown(hero, unsafe_allow_html=True)

    with st.container(key="cardrow"):
        c1, c2, c3 = st.columns(3, gap="medium")

        with c1:
            with st.container(key="card_aw"):
                st.markdown(
                    f'<div class="chead"><div class="cic ic-g">{svg(ICON_CHAT, color="#1f7556", size=30)}</div><div class="ctitle">மோசடி விழிப்புணர்வு</div></div><div class="cdesc">சந்தேகமான அழைப்புகள், SMS, லிங்குகள் பற்றி கேளுங்கள். எளிய தமிழில் விளக்கம் பெறுங்கள்.</div>',
                    unsafe_allow_html=True
                )
                st.button("இப்போதே கேளுங்கள்  →", key="go_aw", on_click=go, args=("aw",))

        with c2:
            with st.container(key="card_dr"):
                st.markdown(
                    f'<div class="chead"><div class="cic ic-r">{svg(ICON_PHONE, color="#a8342a", size=30)}</div><div class="ctitle">Scam Drill (பயிற்சி முறை)</div></div><div class="cdesc">உண்மையான மோசடி அழைப்புகளை போன்ற பயிற்சியில் பங்கேற்று, சரியான பதிலை தேர்ந்தெடுங்கள்.</div>',
                    unsafe_allow_html=True
                )
                st.button("பயிற்சியை தொடங்குங்கள்  →", key="go_dr", on_click=go, args=("dr",))

        with c3:
            with st.container(key="card_gd"):
                st.markdown(
                    f'<div class="chead"><div class="cic ic-b">{svg(ICON_BOOK, color="#1d4e89", size=30)}</div><div class="ctitle">பாதுகாப்பு வழிகாட்டி</div></div><div class="cdesc">பொதுவான டிஜிட்டல் மோசடிகள், அடையாளங்கள் மற்றும் பாதுகாப்பு நடைமுறைகள்.</div>',
                    unsafe_allow_html=True
                )
                st.button("வழிகாட்டியை பார்க்கவும்  →", key="go_gd", on_click=go, args=("gd",))

    st.write("")

    b1, b2 = st.columns([2.3, 1], gap="medium")

    with b1:
        st.markdown(
            '<div class="remember"><h4>💡 நினைவில் கொள்ளுங்கள்!</h4><div class="rem-row">'
            f'<div class="rem">{svg(ICON_LOCK, color="#1f7556")}<span>OTP, PIN, Password<br>யாரிடமும் பகிர வேண்டாம்.</span></div>'
            f'<div class="rem">{svg(ICON_LINK, color="#1f7556")}<span>அறியாத லிங்குகள்<br>கிளிக் செய்ய வேண்டாம்.</span></div>'
            f'<div class="rem">{svg(ICON_FAMILY, color="#1f7556")}<span>சந்தேகம் இருந்தால் உங்கள் குடும்பத்தினருடன் ஆலோசிக்கவும்.</span></div>'
            '</div></div>',
            unsafe_allow_html=True
        )

    with b2:
        st.markdown(
            f'<div class="sos2"><div class="top">{svg(ICON_SHIELD, color="#1f7556", size=26)} சைபர் குற்றம் புகாரளிக்க</div><div class="num">📞 1930</div><small>(தேசிய சைபர் குற்ற உதவி எண்)</small></div>',
            unsafe_allow_html=True
        )


# ───────────────────────── AWARENESS ─────────────────────────
elif page == "aw":

    topbar(
        "விழிப்புணர்வு",
        "மோசடி விழிப்புணர்வு",
        "சந்தேகமான அழைப்பு அல்லது செய்தியா? தமிழில் கேளுங்கள் — பாதுகாப்பான வழிகாட்டுதல் பெறுங்கள்."
    )

    with st.container(key="panel_aw"):
        typed = st.text_input(
            "உங்கள் கேள்வி",
            placeholder="எ.கா. ஒருவர் OTP கேட்கிறார். என்ன செய்ய வேண்டும்?"
        )

        audio = st.audio_input(
            "🎙️ தமிழில் கேள்வியைப் பேசுங்கள்",
            sample_rate=16000,
            key="aw_audio"
        )

        if st.button("🛡️ பாதுகாப்பான பதில் பெறுங்கள்", key="aw_go", use_container_width=True):
            q = typed.strip()

            if audio:
                try:
                    with st.spinner("உங்கள் குரலைப் புரிந்துகொள்கிறேன்…"):
                        q = prisma(audio.getvalue())

                    st.markdown(
                        f'<div class="recog">🎙️ <b>அடையாளம் காணப்பட்ட கேள்வி:</b> {q}</div>',
                        unsafe_allow_html=True
                    )

                except Exception as e:
                    st.error(f"Prisma STT error: {e}")
                    q = ""

            if q:
                st.session_state["aw_answer"] = faq_answer(q)

        if st.session_state.get("aw_answer"):
            st.markdown(
                f'<div class="answer"><small>Arivom AI பதில்</small><p>{st.session_state["aw_answer"]}</p></div>',
                unsafe_allow_html=True
            )

            st.write("")

            if st.button("🔊 பதிலைக் கேளுங்கள்", key="aw_tts"):
                try:
                    with st.spinner("குரல் தயாராகிறது…"):
                        st.audio(
                            timbre(st.session_state["aw_answer"]),
                            format="audio/wav"
                        )

                except Exception as e:
                    st.error(f"Timbre TTS error: {e}")


# ───────────────────────── DRILL ─────────────────────────
elif page == "dr":

    topbar(
        "பயிற்சி",
        "Scam Drill (பயிற்சி முறை)",
        "பாதுகாப்பான சூழலில் பயிற்சி செய்யுங்கள் — உண்மையான மோசடி வரும்போது தயாராக இருப்பீர்கள்."
    )

    with st.container(key="panel_dr"):
        st.info(
            "இவை கற்பனைப் பயிற்சி உரையாடல்கள் மட்டுமே; உண்மையான வங்கி அல்லது நிறுவன அழைப்புகள் அல்ல."
        )
        if GEMINI_API_KEY:
            st.caption("🧠 Gemini AI மதிப்பீடு செயல்படுத்தப்பட்டுள்ளது · Gnani குரல் சேவைகள் தொடர்ந்து பயன்படுத்தப்படுகின்றன.")
        else:
            st.caption("ℹ️ Gemini API key இல்லை; தற்போது keyword fallback மதிப்பீடு பயன்படுத்தப்படும்.")

        idx = st.selectbox(
            "பயிற்சியைத் தேர்ந்தெடுக்கவும்",
            range(len(SCENARIOS)),
            format_func=lambda i: SCENARIOS[i]["title"]
        )

        scenario = SCENARIOS[idx]
        hot = " hot" if scenario["level"] != "Beginner" else ""

        st.markdown(
            f'<span class="chip{hot}">நிலை · {scenario["level"]}</span>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="bubble"><div class="avatar av-bad">📞</div><div class="msg bad"><small>⚠ சந்தேகமான நபர்</small>“{scenario["line"]}”</div></div>',
            unsafe_allow_html=True
        )

        if st.button("🔊 குரலைக் கேளுங்கள்", key="drill_play"):
            try:
                with st.spinner("குரல் தயாராகிறது…"):
                    st.audio(
                        timbre(scenario["line"]),
                        format="audio/wav"
                    )

            except Exception as e:
                st.error(f"Timbre TTS error: {e}")

        st.markdown("**நீங்கள் என்ன பதில் சொல்வீர்கள்?**")

        reply = st.text_input(
            "உங்கள் பதில்",
            placeholder="எ.கா. நான் OTP பகிரமாட்டேன்.",
            key="drill_reply"
        )

        reply_audio = st.audio_input(
            "🎙️ அல்லது குரலில் பதிலளியுங்கள்",
            sample_rate=16000,
            key="drill_mic"
        )

        if st.button("✅ என் பதிலை மதிப்பிடுங்கள்", key="drill_eval", use_container_width=True):
            transcript = reply.strip()

            if reply_audio:
                try:
                    with st.spinner("உங்கள் பதிலைப் புரிந்துகொள்கிறேன்…"):
                        transcript = prisma(reply_audio.getvalue())

                except Exception as e:
                    st.error(f"Prisma STT error: {e}")
                    transcript = ""

            if transcript:
                ok, feedback, evaluation_source = evaluate(scenario, transcript)

                st.session_state["tries"] += 1

                if ok:
                    st.session_state["safe_count"] += 1

                st.session_state["drill_result"] = {
                    "ok": ok,
                    "feedback": feedback,
                    "reply": transcript,
                    "evaluation_source": evaluation_source
                }

        result = st.session_state.get("drill_result")

        if result:
            cls, icon, head = (
                ("good", "✅", "பாதுகாப்பான பதில்!")
                if result["ok"]
                else ("try", "⚠️", "இன்னும் பாதுகாப்பாக பதிலளிக்கலாம்")
            )

            st.markdown(
                f'<div class="bubble"><div class="avatar av-ok">🙂</div><div class="msg ok"><small>உங்கள் பதில்</small>{result["reply"]}</div></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="verdict {cls}"><div class="vi">{icon}</div><div><h4>{head}</h4><p>{result["feedback"]}</p></div></div>',
                unsafe_allow_html=True
            )

            if st.button("🔊 கருத்தைக் கேளுங்கள்", key="drill_feedback"):
                try:
                    with st.spinner("குரல் தயாராகிறது…"):
                        st.audio(
                            timbre(result["feedback"]),
                            format="audio/wav"
                        )

                except Exception as e:
                    st.error(f"Timbre TTS error: {e}")


# ───────────────────────── GUIDE ─────────────────────────
elif page == "gd":

    topbar(
        "வழிகாட்டி",
        "பாதுகாப்பு வழிகாட்டி",
        "பொதுவான டிஜிட்டல் மோசடிகள், அடையாளங்கள் மற்றும் பாதுகாப்பு நடைமுறைகள்."
    )

    for question, answer, _ in FAQ:
        with st.expander("🛡️  " + question):
            st.write(answer)

    st.markdown(
        '<div class="sos2" style="margin-top:16px">'
        '<div class="top">🛡️ பணம் இழந்துவிட்டீர்களா? உடனே வங்கியைத் தொடர்புகொள்ளுங்கள்</div>'
        '<div class="num">📞 1930</div>'
        '<small>தேசிய சைபர் குற்ற உதவி எண் · புகார்: cybercrime.gov.in</small>'
        '</div>',
        unsafe_allow_html=True
    )


# ───────────────────────── PROGRESS ─────────────────────────
elif page == "pg":

    topbar(
        "முன்னேற்றம்",
        "என் முன்னேற்றம்",
        "உங்கள் Scam Drill பயிற்சி முடிவுகள் (இந்த session-க்கு மட்டும்)."
    )

    t, s = st.session_state["tries"], st.session_state["safe_count"]
    pct = int(100 * s / t) if t else 0

    st.markdown(
        '<div class="score">'
        f'<div class="stat"><div><b>{t}</b><span>முயற்சிகள்</span></div></div>'
        f'<div class="stat"><div><b>{s}</b><span>பாதுகாப்பான பதில்கள்</span></div></div>'
        f'<div class="stat"><div class="ring" style="background:conic-gradient(#2a7d5d {pct * 3.6}deg,#e3ece5 0)"><b>{pct}%</b></div>'
        '<div><b style="font-size:18px">பாதுகாப்பு மதிப்பெண்</b><span>உங்கள் துல்லியம்</span></div></div>'
        '</div>',
        unsafe_allow_html=True
    )

    def bd(on, txt):
        return f'<div class="bdg {"on" if on else "off"}">{txt}</div>'

    st.markdown("**பதக்கங்கள்**")

    st.markdown(
        '<div class="badges2">'
        + bd(t >= 1, "🌱 முதல் பயிற்சி")
        + bd(s >= 1, "🛡️ முதல் பாதுகாப்பான பதில்")
        + bd(s >= 3, "⭐ 3 பாதுகாப்பான பதில்கள்")
        + bd(t >= 4 and pct >= 75, "🏆 மோசடி எதிர்ப்பு வீரர்")
        + '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.button(
        "📞 மேலும் பயிற்சி செய்யுங்கள்  →",
        key="more_drill",
        on_click=go,
        args=("dr",)
    )


# ───────────────────────── FOOTER ─────────────────────────
st.markdown(
    '<div class="foot">ARIVOM AI · அறிவோம். விழிப்போம். பாதுகாப்போம். | கல்வி மற்றும் விழிப்புணர்வுக்கான prototype · Powered by Gnani Vachana</div>',
    unsafe_allow_html=True
)