import praw
import datetime

reddit = praw.Reddit(
    client_id     = "SEU_CLIENT_ID",
    client_secret = "SEU_CLIENT_SECRET",
    user_agent    = "LumiSolo/1.0 Research Scraper (by u/seu_usuario)"
)

# Janelas de data como timestamps Unix (filtro pós-coleta)
TS_2020 = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
TS_2021 = datetime.datetime(2021, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
TS_2022 = datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
TS_END  = datetime.datetime(2026, 6, 13, tzinfo=datetime.timezone.utc).timestamp()
results_R01 = reddit.subreddit(
    "agronegocio+agricultura+fazenda+brasil"
).search(
    query       = 'fertilizante "preço" "caro" problema',
    sort        = "top",
    time_filter = "all",
    limit       = 1000
)

# ── FILTROS PÓS-COLETA ──────────────────────────────────────────
# item.score          >= 2
# item.created_utc    in [TS_2022, TS_END]
# NOT item.author.name in ["AutoModerator", "[deleted]"]
# NOT "patrocinado" OR "publi" OR "afiliado" in item.selftext (anti-spam)
# ─────────────────────────────────────────────────────────────────

results_R02 = reddit.subreddit(
    "agronegocio+agricultura"
).search(
    query       = '"insumo agrícola" OR "insumos agrícolas" "onde comprar" OR recomendação',
    sort        = "relevance",
    time_filter = "all",
    limit       = 500
)

# ── FILTROS PÓS-COLETA ──────────────────────────────────────────
# item.score          >= 1
# item.created_utc    in [TS_2021, TS_END]
# NOT item.link_flair_text == "PUBLICIDADE"
# item.author.comment_karma >= 10  (reduz contas novas/spam)
# ─────────────────────────────────────────────────────────────────

results_R03 = reddit.subreddit(
    "agronegocio+agricultura+brasil"
).search(
    query       = '"análise de solo" fertilizante OR adubo recomendação NPK',
    sort        = "relevance",
    time_filter = "all",
    limit       = 500
)

# ── FILTROS PÓS-COLETA ──────────────────────────────────────────
# item.score          >= 1
# item.created_utc    in [TS_2020, TS_END]
# NOT "jardinagem" OR "plantas ornamentais" in item.selftext  (evita horticultura urbana)
# ─────────────────────────────────────────────────────────────────

results_R04 = reddit.subreddit(
    "brasil+agronegocio"
).search(
    query       = 'perdas lavoura "insumo errado" OR "solo inadequado" OR "produto errado" prejuízo',
    sort        = "top",
    time_filter = "all",
    limit       = 500
)

# ── FILTROS PÓS-COLETA ──────────────────────────────────────────
# item.score          >= 2
# item.created_utc    in [TS_2021, TS_END]
# len(item.selftext)  >= 100  (prioriza posts com narrativa detalhada)
# ─────────────────────────────────────────────────────────────────

results_R05 = reddit.subreddit(
    "empreendedorismo+startupsbrasil"
).search(
    query       = 'agtech agronegócio marketplace "insumo" startup',
    sort        = "top",
    time_filter = "all",
    limit       = 300
)

# ── FILTROS PÓS-COLETA ──────────────────────────────────────────
# item.score          >= 3
# item.created_utc    in [TS_2022, TS_END]
# NOT "cripto" OR "blockchain" OR "NFT" in item.selftext  (evita ruído de hype tech)
# ─────────────────────────────────────────────────────────────────

results_R06 = reddit.subreddit(
    "agronegocio+agricultura"
).search(
    query       = 'digitalização tecnologia app "produtor rural" OR "agricultor" OR "fazendeiro"',
    sort        = "relevance",
    time_filter = "all",
    limit       = 500
)

# ── FILTROS PÓS-COLETA ──────────────────────────────────────────
# item.score          >= 1
# item.created_utc    in [TS_2022, TS_END]
# NOT "agropecuária esporte" OR "rural show" in item.selftext
# ─────────────────────────────────────────────────────────────────