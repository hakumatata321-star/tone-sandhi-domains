import hashlib, hmac
from pathlib import Path
import numpy as np

N_CLASS, N_SYLL, P_T3 = 8, 140, 0.58
LEN_MIN, LEN_MAX = 10, 20
THETA, RATE_SHIFT, MS_PER_SYLL, DUR_NOISE = 0.55, 0.12, 230.0, 0.06
N_SPEAKERS, UTTERANCES_PER_SPEAKER = 1000, 12
SPEAKER_BINDING_SD, SPEAKER_THRESHOLD_SD = 0.10, 0.06
ONSET = ["b", "p", "m", "f", "d", "t", "n", "l", "g", "k", "h", "j", "q", "x", "zh", "ch", "sh", "r", "z", "c", "s", ""]
RIME = ["a", "o", "e", "ai", "ei", "ao", "ou", "an", "en", "ang", "eng", "i", "ia", "ie", "iao", "iu", "ian", "in",
        "iang", "ing", "u", "ua", "uo", "uai", "ui", "uan", "un", "uang", "ong", "v", "ue", "un"]


def load_secret():
    return Path(__file__).resolve().parent.joinpath("SECRET_DO_NOT_SHARE.txt").read_text().strip().encode()


def _h(key, *parts):
    return hmac.new(key, "|".join(map(str, parts)).encode(), hashlib.sha256).digest()


def krng(key, *parts):
    return np.random.default_rng(int.from_bytes(_h(key, *parts)[:8], "big"))


def kid(key, *parts):
    return _h(key, *parts).hex()[:10]


def lexicon(key):
    rng = krng(key, "lex")
    forms, seen = [], set()
    while len(forms) < N_SYLL:
        f = ONSET[rng.integers(len(ONSET))] + RIME[rng.integers(len(RIME))]
        if f and f not in seen:
            seen.add(f); forms.append(f)
    cls = rng.integers(0, N_CLASS, N_SYLL)
    tone = np.where(rng.random(N_SYLL) < P_T3, 3, rng.choice([0, 1, 2, 4], N_SYLL, p=[0.08, 0.28, 0.26, 0.38]))
    return forms, cls, tone


def bindings(key):
    rng = krng(key, "bind")
    B = rng.uniform(0.0, 1.0, (N_CLASS, N_CLASS))
    for _ in range(N_CLASS * 2):
        i, j = rng.integers(0, N_CLASS, 2)
        B[i, j] = 1.0 if rng.random() < 0.5 else 0.0
    return B


def speaker(key, s, B):
    rng = krng(key, "speaker", s)
    Bs = np.clip(B + SPEAKER_BINDING_SD * rng.standard_normal(B.shape), 0.0, 1.0)
    return Bs, THETA + SPEAKER_THRESHOLD_SD * float(rng.standard_normal())


def bracket(cls_seq, B, theta):
    nodes, heads = list(range(len(cls_seq))), list(cls_seq)
    while len(nodes) > 1:
        best, bi = -1.0, -1
        for i in range(len(nodes) - 1):
            s = B[heads[i], heads[i + 1]]
            if s > best:
                best, bi = s, i
        if best < theta:
            break
        nodes[bi:bi + 2] = [(nodes[bi], nodes[bi + 1])]
        heads[bi:bi + 2] = [heads[bi]]
    return nodes


def sandhi(domains, tone):
    out = list(tone)

    def apply(node):
        if isinstance(node, int):
            return [node]
        span = apply(node[0]) + apply(node[1])
        for a, b in zip(span, span[1:]):
            if out[a] == 3 and out[b] == 3:
                out[a] = 2
        return span

    for d in domains:
        apply(d)
    return out


def speaker_utterances(key, s):
    forms, cls, ltone = lexicon(key)
    Bs, theta_s = speaker(key, s, bindings(key))
    sid = "p_" + kid(key, "speaker", s)
    out = []
    for k in range(UTTERANCES_PER_SPEAKER):
        rng = krng(key, "utterance", s, k)
        n = int(rng.integers(LEN_MIN, LEN_MAX + 1)); idx = rng.integers(0, N_SYLL, n)
        cseq = [int(cls[j]) for j in idx]; tseq = [int(ltone[j]) for j in idx]
        z = float(rng.standard_normal())
        dur = n * MS_PER_SYLL * float(np.exp(-0.10 * z + DUR_NOISE * rng.standard_normal()))
        surf = sandhi(bracket(cseq, Bs, theta_s - RATE_SHIFT * z), tseq)
        out.append({"case_id": "u_" + kid(key, "utterance", s, k), "speaker_id": sid, "syll": [forms[j] for j in idx], "cls": cseq,
                    "under": tseq, "surface": surf, "duration_ms": int(round(dur))})
    return out
