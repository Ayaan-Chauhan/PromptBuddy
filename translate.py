import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

# Language Mapping
LANG_CODE_MAP = {
    "english": "eng_Latn",
    "hindi": "hin_Deva",
    "marathi": "mar_Deva",
    "tamil": "tam_Taml",
    "telugu": "tel_Telu",
    "kannada": "kan_Knda",
    "bengali": "ben_Beng",
    "punjabi": "pan_Guru",
    "gujarati": "guj_Gujr",
    "malayalam": "mal_Mlym",
    "odia": "ory_Orya",
    "assamese": "asm_Beng",
    "urdu": "urd_Arab",
}

SUPPORTED_LANGUAGE_CODES = list(LANG_CODE_MAP.values())
INDIC_CODES = set([v for v in SUPPORTED_LANGUAGE_CODES if not v.startswith("eng")])

# Device Setup
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load Models Once
print("[INFO] Loading IndicTrans2 translation models...")

en_indic_model_name = "ai4bharat/indictrans2-en-indic-1B"
indic_en_model_name = "ai4bharat/indictrans2-indic-en-1B"

en_indic_tokenizer = AutoTokenizer.from_pretrained(en_indic_model_name, trust_remote_code=True)
en_indic_model = AutoModelForSeq2SeqLM.from_pretrained(en_indic_model_name, trust_remote_code=True).to(DEVICE)

indic_en_tokenizer = AutoTokenizer.from_pretrained(indic_en_model_name, trust_remote_code=True)
indic_en_model = AutoModelForSeq2SeqLM.from_pretrained(indic_en_model_name, trust_remote_code=True).to(DEVICE)

ip = IndicProcessor(inference=True)

# Translation Function (for FastAPI)
def run_translation(text: str, src_lang: str, tgt_lang: str) -> str:
    """Translate text between English and Indic languages using IndicTrans2."""

    if src_lang == "eng_Latn" and tgt_lang in INDIC_CODES:
        model, tokenizer = en_indic_model, en_indic_tokenizer
    elif tgt_lang == "eng_Latn" and src_lang in INDIC_CODES:
        model, tokenizer = indic_en_model, indic_en_tokenizer
    else:
        raise ValueError("Unsupported translation direction. Only English ↔ Indic supported.")

    # Preprocess
    batch = ip.preprocess_batch([text], src_lang=src_lang, tgt_lang=tgt_lang)
    inputs = tokenizer(batch, padding="longest", return_tensors="pt", truncation=True).to(DEVICE)

    # Translate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            use_cache=True,
            min_length=0,
            max_length=256,
            num_beams=5,
            num_return_sequences=1,
        )

    # Postprocess
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    translated = ip.postprocess_batch(decoded, lang=tgt_lang)
    return translated[0]
