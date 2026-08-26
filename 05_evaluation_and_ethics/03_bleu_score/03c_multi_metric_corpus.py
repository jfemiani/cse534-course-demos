"""Demo: a real summarization benchmark, scored with BLEU, ROUGE-L,
METEOR, and BERTScore (via nltk, rouge-score, and bert-score) against a
real human reference summary instead of an invented one.

Two bills from BillSum (Kornilova and Eidelman, "BillSum: A Corpus for
Automatic Summarization of US Legislation," 2019,
https://huggingface.co/datasets/FiscalNote/billsum) are summarized by
ChatGPT, then scored against BillSum's own human-written reference
summary for that bill.

See 03c_multi_metric_corpus.md for the full explanation.
"""

import os

import nltk
from bert_score import BERTScorer
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.translate.meteor_score import meteor_score
from openai import OpenAI
from rouge_score import rouge_scorer

nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
rouge = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
bert_scorer = BERTScorer(model_type=MODEL_NAME, num_layers=6, lang="en", rescale_with_baseline=False)

# Two real BillSum test-set bills (public domain, US Government Publishing
# Office). Each "reference_summary" below is BillSum's own human-written
# summary, not something written for this demo.
BILLS = [
    {
        "title": "Merchant Marine of World War II Congressional Gold Medal Act",
        "text": (
            "SECTION 1. SHORT TITLE.\n\n"
            "    This Act may be cited as the ``Merchant Marine of World War II "
            "Congressional Gold Medal Act''.\n\n"
            "SEC. 2. FINDINGS.\n\n"
            "    The Congress finds the following:\n"
            "        (1) The United States Merchant Marine was integral in "
            "providing the link between domestic production and the fighting "
            "forces overseas, providing combat equipment, fuel, food, "
            "commodities, and raw materials to troops stationed overseas.\n"
            "        (2) The United States Merchant Marine provided for the "
            "successful transport of resources and personnel despite "
            "consistent and ongoing exposure to enemy combatants from both "
            "the air and the sea, such as enemy bomber squadrons, "
            "submarines, and mines.\n"
            "        (3) The efforts of the United States Merchant Marine were "
            "not without sacrifices as they bore a higher per capita "
            "casualty rate than any other branch of the military during the "
            "war.\n"
            "        (4) The feats and accomplishments of the Merchant Marine "
            "are deserving of broader public recognition.\n\n"
            "SEC. 3. CONGRESSIONAL GOLD MEDAL.\n\n"
            "    (a) Award Authorized.--The Speaker of the House of Representatives "
            "and the President pro tempore of the Senate shall make appropriate "
            "arrangements for the award, on behalf of the Congress, of a single gold "
            "medal of appropriate design to the U.S. Merchant Marine of World War "
            "II, in recognition of their dedicated and vital service during World "
            "War II.\n"
            "    (b) Design and Striking.--For the purposes of the award referred to "
            "in subsection (a), the Secretary of the Treasury shall strike the gold "
            "medal with suitable emblems, devices, and inscriptions.\n"
            "    (c) American Merchant Marine Museum.--Following the award of the "
            "gold medal in honor of the U.S. Merchant Marine, the gold medal shall "
            "be given to the American Merchant Marine Museum, where it will be "
            "available for display as appropriate and available for research.\n\n"
            "SEC. 4. DUPLICATE MEDALS.\n\n"
            "    Under such regulations as the Secretary may prescribe, the "
            "Secretary may strike and sell duplicates in bronze of the gold medal "
            "struck under section 3, at a price sufficient to cover the costs of the "
            "medals, including labor, materials, dies, use of machinery, and "
            "overhead expenses.\n\n"
            "SEC. 5. STATUS OF MEDALS.\n\n"
            "    (a) National Medals.--Medals struck pursuant to this Act are "
            "national medals for purposes of chapter 51 of title 31, United States "
            "Code.\n"
            "    (b) Numismatic Items.--For purposes of section 5134 of title 31, "
            "United States Code, all medals struck under this Act shall be "
            "considered to be numismatic items."
        ),
        "reference_summary": (
            "Merchant Marine of World War II Congressional Gold Medal Act "
            "(Sec. 3) This bill requires the Speaker of the House of Representatives "
            "and the President pro tempore of the Senate to arrange for the award, "
            "on behalf of Congress, of a single gold medal to the U.S. Merchant "
            "Marine of World War II, in recognition of their dedicated and vital "
            "service during World War II. Following its award the medal shall be "
            "given to the American Merchant Marine Museum where it will be available "
            "for display and research."
        ),
    },
    {
        "title": "Prescription Drug Monitoring Act of 2016",
        "text": (
            "SECTION 1. SHORT TITLE.\n\n"
            "    This Act may be cited as the ``Prescription Drug Monitoring Act of "
            "2016''.\n\n"
            "SEC. 3. PRESCRIPTION DRUG MONITORING PROGRAM REQUIREMENTS.\n\n"
            "    (a) In General.--Beginning 2 years after the date of enactment of "
            "this Act, each covered State shall require--\n"
            "        (1) each prescribing practitioner within the covered State "
            "or their designee to consult the PDMP of the covered State "
            "before initiating treatment with a prescription for a "
            "controlled substance listed in schedule II, III, or IV, and every 3 "
            "months thereafter as long as the treatment continues;\n"
            "        (2) the PDMP of the covered State to provide proactive "
            "notification to a practitioner when patterns indicative of "
            "controlled substance misuse, including opioid misuse, are "
            "detected;\n"
            "        (3) each dispenser within the covered State to report each "
            "prescription for a controlled substance dispensed by the "
            "dispenser to the PDMP not later than 24 hours after the "
            "controlled substance is dispensed to the patient; and\n"
            "        (4) that the PDMP make available a quarterly de-identified "
            "data set and an annual report for public and private use.\n"
            "    (b) Noncompliance.--If a covered State fails to comply with "
            "subsection (a), the Attorney General or the Secretary of Health and "
            "Human Services, as appropriate, may withhold grant funds from being "
            "awarded to the covered State under the Harold Rogers Prescription Drug "
            "Monitoring Program or the controlled substance monitoring program.\n\n"
            "SEC. 4. SHARING PDMP INFORMATION AMONG STATES.\n\n"
            "    (a) Requirement.--Beginning 2 years after the date of enactment of "
            "this Act, each covered State shall make the data contained in the PDMP "
            "of the covered State available to other States through the data-sharing "
            "single technology solution established under subsection (b).\n"
            "    (b) Data-Sharing Single Technology Solution.--The Attorney General, "
            "in coordination with the Secretary of Health and Human Services, shall "
            "award, on a competitive basis, a grant to an eligible entity to "
            "establish and maintain an inter-State data-sharing single hub to "
            "facilitate the sharing of PDMP data among States and the accessing of "
            "such data by practitioners. The hub shall allow States to retain "
            "ownership of the data they submit, provide de-identified data for "
            "research, and allow authorized users to access data without a user fee."
        ),
        "reference_summary": (
            "Prescription Drug Monitoring Act of 2016 This bill requires a state "
            "that receives grant funds under the prescription drug monitoring "
            "program (PDMP) or the controlled substance monitoring program to "
            "comply with specified requirements. The Department of Justice (DOJ) or "
            "Department of Health and Human Services may withhold grant funds from "
            "a state that fails to comply. Additionally, the bill requires a state "
            "to share its PDMP data with other states through a data-sharing hub "
            "established by DOJ."
        ),
    },
]


def summarize(bill_text: str) -> str:
    prompt = (
        "Summarize the following US Congressional bill in one paragraph, "
        "the way a legislative summary service would: state what the bill "
        "does, not how it is worded.\n\n" + bill_text
    )
    return client.responses.create(model=model, input=prompt).output_text.strip()


def bleu(reference: str, candidate: str) -> float:
    ref_tokens, cand_tokens = reference.lower().split(), candidate.lower().split()
    return sentence_bleu([ref_tokens], cand_tokens, smoothing_function=SmoothingFunction().method1)


def rouge_l(reference: str, candidate: str) -> float:
    return rouge.score(reference, candidate)["rougeL"].fmeasure


def meteor(reference: str, candidate: str) -> float:
    ref_tokens, cand_tokens = reference.lower().split(), candidate.lower().split()
    return meteor_score([ref_tokens], cand_tokens)


def bertscore(reference: str, candidate: str) -> float:
    _, _, f1 = bert_scorer.score([candidate], [reference])
    return f1.item()


print(f"{'bill':<45s} {'BLEU':>7s} {'ROUGE-L':>8s} {'METEOR':>7s} {'BERTScore':>10s}")
for bill in BILLS:
    generated_summary = summarize(bill["text"])
    reference = bill["reference_summary"]
    b = bleu(reference, generated_summary)
    r = rouge_l(reference, generated_summary)
    m = meteor(reference, generated_summary)
    s = bertscore(reference, generated_summary)
    print(f"{bill['title'][:45]:<45s} {b:7.3f} {r:8.3f} {m:7.3f} {s:10.3f}")
    print(f"  reference: {reference}")
    print(f"  chatgpt:   {generated_summary}\n")
