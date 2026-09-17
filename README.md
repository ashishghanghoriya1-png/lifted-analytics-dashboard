# LiftED dashboard

Run `streamlit run app.py`.

## Programme Intelligence Digest

The digest follows the zone selector and includes a separate brief for each selected zone. It analyses the zone-level snapshot embedded in `ZONE_FLN_DATA` (week ending 11 September 2026), not live or externally researched statistics. Other slicers do not alter this zone-level brief.

`zone_briefs.json` ships with the app so hosted deployments do not need access to a developer's local files or an Ollama server. Each brief records its model, generation time and source fingerprint. Changed data or missing briefs show a clearly labelled data summary instead of an outdated AI assessment.

To regenerate after changing the data, start local Ollama and run:

```powershell
python generate_zone_briefs.py --model qwen3.5:4b-q4_K_M
```

Review generated statements against the source before committing `zone_briefs.json`. Generation uses the local Ollama API; no API token is required. No automatic weekly refresh is configured.

The dashboard retains its light report surfaces in System/Light/Dark modes, with explicit readable labels and chart colors. Native input controls and menus retain Streamlit's selected theme.
