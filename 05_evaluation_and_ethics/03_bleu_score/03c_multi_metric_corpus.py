"""Demo: zero-shot vs. one-shot prompting on a real summarization
benchmark, scored with BLEU, ROUGE-L, METEOR, and BERTScore (via nltk,
rouge-score, and bert-score) against real human reference summaries
instead of invented ones.

Two bills from BillSum (Kornilova and Eidelman, "BillSum: A Corpus for
Automatic Summarization of US Legislation," 2019,
https://huggingface.co/datasets/FiscalNote/billsum) are each summarized by
ChatGPT twice: once with a zero-shot prompt (no example) and once with a
one-shot prompt that includes one worked example -- a third, different
bill and its real BillSum summary. Each generated summary is scored
against BillSum's own human-written reference summary for that bill, and
the two scores per bill are averaged into one row per prompt.

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

# A third real BillSum bill (public domain, US Government Publishing
# Office), used only as the worked example inside the one-shot prompt
# below. It is never itself summarized or scored.
EXAMPLE_BILL = {
    "title": "Children's Bicycle Helmet Safety Act of 1993",
    "text": (
        "SECTION 1. SHORT TITLE.\n\n"
        "    This Act may be cited as the ``Children's Bicycle Helmet Safety Act "
        "of 1993''.\n\n"
        "SEC. 2. FINDINGS.\n\n"
        "    The Congress finds that--\n"
        "        (1) 90 million Americans ride bicycles and 20 million ride "
        "a bicycle more than once a week;\n"
        "        (2) between 1984 and 1988, 2,985 bicyclists in the United "
        "States died from head injuries and 905,752 suffered head injuries "
        "that were treated in hospital emergency rooms;\n"
        "        (3) 41 percent of bicycle-related head injury deaths and 76 "
        "percent of bicycle-related head injuries occurred among American "
        "children under age 15;\n"
        "        (4) deaths and injuries from bicycle accidents cost society "
        "$7.6 billion annually; and a child suffering from a head injury, on "
        "average, will cost society $4.5 million over the child's lifetime;\n"
        "        (5) universal use of bicycle helmets in the United States "
        "would have prevented 2,600 deaths from head injuries and 757,000 "
        "injuries; and\n"
        "        (6) only 5 percent of children in the Nation who ride "
        "bicycles wear helmets.\n\n"
        "SEC. 3. ESTABLISHMENT OF PROGRAM.\n\n"
        "    The Administrator of the National Highway Traffic Safety "
        "Administration may, in accordance with section 4, make grants to "
        "States, State political subdivisions, and nonprofit organizations for "
        "programs that require or encourage individuals under the age of 16 to "
        "wear approved bicycle helmets. In making those grants, the "
        "Administrator shall allow grantees to use wide discretion in designing "
        "programs that effectively promote increased bicycle helmet use.\n\n"
        "SEC. 4. PURPOSES FOR GRANTS.\n\n"
        "    A grant made under section 3 may be used by a grantee to--\n"
        "        (1) enforce a law that requires individuals under the age "
        "of 16 to wear approved bicycle helmets on their heads while riding "
        "on bicycles;\n"
        "        (2) assist individuals under the age of 16 to acquire "
        "approved bicycle helmets;\n"
        "        (3) develop and administer a program to educate individuals "
        "under the age of 16 and their families on the importance of wearing "
        "such helmets in order to improve bicycle safety; or\n"
        "        (4) carry out any combination of the activities described "
        "in paragraphs (1), (2), and (3).\n\n"
        "SEC. 5. STANDARDS.\n\n"
        "    (a) In General.--Bicycle helmets manufactured 9 months or more "
        "after the date of the enactment of this Act shall conform to--\n"
        "        (1) any interim standard described under subsection (b), "
        "pending the establishment of a final standard pursuant to "
        "subsection (c); and\n"
        "        (2) the final standard, once it has been established under "
        "subsection (c).\n"
        "    (b) Interim Standards.--The interim standards are as follows:\n"
        "        (1) The American National Standards Institute standard "
        "designated as ``Z90.4-1984''.\n"
        "        (2) The Snell Memorial Foundation standard designated as "
        "``B-90''.\n"
        "        (3) Any other standard that the Consumer Product Safety "
        "Commission determines is appropriate.\n"
        "    (c) Final Standard.--Not later than 60 days after the date of the "
        "enactment of this Act, the Consumer Product Safety Commission shall "
        "begin a proceeding under section 553 of title 5, United States Code, "
        "to--\n"
        "        (1) review the requirements of the interim standards set "
        "forth in subsection (a) and establish a final standard based on "
        "such requirements;\n"
        "        (2) include in the final standard a provision to protect "
        "against the risk of helmets coming off the heads of bicycle riders;\n"
        "        (3) include in the final standard provisions that address "
        "the risk of injury to children; and\n"
        "        (4) include additional provisions as appropriate.\n"
        "Sections 7 and 9 of the Consumer Product Safety Act (15 U.S.C. 2056 and "
        "2058) shall not apply to the proceeding under this subsection and "
        "section 11 of such Act (15 U.S.C. 2060) shall not apply with respect to "
        "any standard issued under such proceeding. The final standard shall "
        "take effect 1 year from the date it is issued.\n"
        "    (d) Failure To Meet Standards.--\n"
        "        (1) Failure to meet interim standard.--Until the final "
        "standard takes effect, a bicycle helmet that does not conform to an "
        "interim standard as required under subsection (a)(1) shall be "
        "considered in violation of a consumer product safety standard "
        "promulgated under the Consumer Product Safety Act.\n"
        "        (2) Status of final standard.--The final standard developed "
        "under subsection (c) shall be considered a consumer product safety "
        "standard promulgated under the Consumer Product Safety Act.\n\n"
        "SEC. 6. AUTHORIZATION OF APPROPRIATIONS.\n\n"
        "    For the National Highway Traffic Safety Administration to carry out "
        "the grant program authorized by this Act, there are authorized to be "
        "appropriated $2,000,000 for fiscal year 1994, $3,000,000 for fiscal "
        "year 1995, and $4,000,000 for fiscal year 1996.\n\n"
        "SEC. 7. DEFINITION.\n\n"
        "    In this Act, the term ``approved bicycle helmet'' means a bicycle "
        "helmet that meets--\n"
        "        (1) any interim standard described in section 5(b), pending "
        "establishment of a final standard under section 5(c); and\n"
        "        (2) the final standard, once it is established under "
        "section 5(c)."
    ),
    "reference_summary": (
        "Children's Bicycle Helmet Safety Act of 1993 - Authorizes the "
        "Administrator of the National Highway Traffic Safety Administration "
        "to make grants to States, political subdivisions, and nonprofit "
        "organizations for programs that require or encourage individuals "
        "under age 16 to wear approved bicycle helmets. Specifies that such "
        "grants may be used to: (1) enforce a law that requires such "
        "individuals to wear approved bicycle helmets; (2) assist such "
        "individuals to acquire such helmets; and (3) develop and administer "
        "a program to educate such individuals and their families on the "
        "importance of wearing such helmets. Sets interim standards for "
        "bicycle helmets and provides that a helmet that does not conform "
        "shall be considered in violation of a consumer product safety "
        "standard promulgated under the Consumer Product Safety Act (CPSA). "
        "Directs the Consumer Product Safety Commission to begin a proceeding "
        "to review the requirements of the interim standards and establish a "
        "final standard that includes provisions to protect against the risk "
        "of helmets coming off the heads of bicycle riders and to address the "
        "risk of injury to children. Specifies that the final standard shall "
        "be considered a consumer product safety standard under the CPSA. "
        "Authorizes appropriations."
    ),
}

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


INSTRUCTIONS = (
    "Summarize the following US Congressional bill in one paragraph, "
    "the way a legislative summary service would: state what the bill "
    "does, not how it is worded.\n\n"
)


def summarize_zero_shot(bill_text: str) -> str:
    prompt = INSTRUCTIONS + bill_text
    return client.responses.create(model=model, input=prompt).output_text.strip()


def summarize_one_shot(bill_text: str) -> str:
    prompt = (
        INSTRUCTIONS
        + "Here is an example of a bill and its summary:\n\n"
        + f"BILL:\n{EXAMPLE_BILL['text']}\n\n"
        + f"SUMMARY:\n{EXAMPLE_BILL['reference_summary']}\n\n"
        + "Now summarize this bill the same way:\n\n"
        + bill_text
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


PROMPTS = {
    "zero-shot (no example)": summarize_zero_shot,
    "one-shot (one example)": summarize_one_shot,
}

results = {}
for prompt_name, summarize in PROMPTS.items():
    scores = {"BLEU": [], "ROUGE-L": [], "METEOR": [], "BERTScore": []}
    print(f"=== {prompt_name} ===")
    for bill in BILLS:
        generated_summary = summarize(bill["text"])
        reference = bill["reference_summary"]
        scores["BLEU"].append(bleu(reference, generated_summary))
        scores["ROUGE-L"].append(rouge_l(reference, generated_summary))
        scores["METEOR"].append(meteor(reference, generated_summary))
        scores["BERTScore"].append(bertscore(reference, generated_summary))
        print(f"  {bill['title']}")
        print(f"    reference: {reference}")
        print(f"    chatgpt:   {generated_summary}\n")
    results[prompt_name] = {metric: sum(vals) / len(vals) for metric, vals in scores.items()}

print(f"{'prompt':<28s} {'BLEU':>7s} {'ROUGE-L':>8s} {'METEOR':>7s} {'BERTScore':>10s}")
for prompt_name, avg in results.items():
    print(
        f"{prompt_name:<28s} {avg['BLEU']:7.3f} {avg['ROUGE-L']:8.3f} "
        f"{avg['METEOR']:7.3f} {avg['BERTScore']:10.3f}"
    )
