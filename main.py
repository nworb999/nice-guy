import logging
from enum import Enum
from llm_handler import start_tunnel, stop_tunnel, get_response

IMAGINATION_IP = "imagination.mat.ucsb.edu"
IMAGINATION_PORT = 11434
LOCAL_PORT = 12345
SSH_USERNAME = "emma"
SSH_KEYFILE = "~/.ssh/id_rsa"

URL = f"http://localhost:{LOCAL_PORT}/api/chat"

QUESTION_1 = """
In the story, did somebody say something they should not have said?
"""

QUESTION_2 = """
What did the person say that they should not have said?
"""

QUESTION_1_RESTRICTED = """Answer with “Yes” or “No” only, without explanations. In case of doubt, answer
according to the most probable answer."""

QUESTION_2_RESTRICTED = """Answer with a quote only, without explanations."""

QUESTION_3_RESTRICTED = """Answer the question only, without explanations."""

QUESTION_4_RESTRICTED = """Answer with “Yes” or “No” only, without explanations. In case of doubt, answer
according to the most probable answer."""


FAUX_PAS_PROMPTS = [
    {
        "prompt": """
        Mike was in one of the cubicles in the toilets at
    school. Joe and Peter were at the sinks nearby. Joe
    said "You know that new boy in the class, his name
    is Mike. Doesn't he look really weird!" Mike then
    came out of the cubicles. Peter said "Oh hello
    Mike, are you going to play football now?".
    """,
        "question_1": QUESTION_1,
        "question_2": QUESTION_2,
        "question_3": "Where were Joe and Peter when they were talking?",
        "question_4": "Did Joe Know that Mike was in the cubicles?",
    },
    {
        "prompt": """
        Jill had just moved into a new house. She went
    shopping with her Mum and bought some new curtains. When Jill had just put them up, her best
    friend Lisa came round and said, "Oh, those curtains are horrible, I hope you're going to get some
    new ones." Jill asked, "Do you like the rest of my
    bedroom?."
    """,
        "question_1": QUESTION_1,
        "question_2": QUESTION_2,
        "question_3": "What had Jill just bought?",
        "question_4": "Did Lisa know the curtains were new?",
    },
    {
        "prompt": """
        All of the class took part in a story competition.
    Emma really wanted to win. Whilst she was away
    from school, the results of the competition were
    announced: Alice was the winner. The next day,
    Alice saw Emma and said "I'm sorry about your
    story." "What do you mean?" said Emma. "Oh
    nothing," said Alice.
    """,
        "question_1": QUESTION_1,
        "question_2": QUESTION_2,
        "question_3": "Who won the story competition?",
        "question_4": "Did Alice realize that Emma hadn't heard the results of the competition?",
        "feedback": """
        Alice said something wrong by assuming that Emma knew the results of the
    competition.  She told Emma that she was sorry about her story, which made Emma confused
    because she didn't know the results, and she would have preferred to find out that she
    hadn't won in a different way.  Alice won the story competition.  She realized that 
    Emma hadn't heard the results of the competition yet.'
          """,
    },
    {
        "prompt": """
        Tim was in a restaurant. He spilt his coffee on the
    floor by accident. Jack was another person in the
    restaurant, standing by the cash desk waiting to
    pay. Tim went up to Jack and said "I'm terribly
    sorry, but I've spilt my coffee. Would you be able
    to mop it up?"
    """,
        "question_1": QUESTION_1,
        "question_2": QUESTION_2,
        "question_3": "Where did the story take place?",
        "question_4": "Did Tim know Jack was a customer?",
    },
]

CONTROL_PROMPTS = [
    {
        "prompt": """
        John was in one of the cubicles in the toilets at
    school. Sam and Eddy were at the sinks nearby.
    Sam said "You know that new boy in the class—
    you know, his name is John. Doesn't he look cool!"
    John then came out of the cubicles. Peter said "Oh,
    hi John. Are you going to play football now?"
    """,
        "question_1": QUESTION_1,
        "question_2": QUESTION_2,
        "question_3": "Where were Sam and Eddy when they were talking?",
        "question_4": "Did Sam Know that John was in the cubicles?",
        "feedback": "",
    },
    {
        "prompt": """
        Michelle had just moved into a new house. Michelle
    went shopping with her Mum and bought a new rug
    for her bedroom. When Michelle had just put it
    down, her best friend, Samantha, came round and
    said, "Oh, your new rug is just like my new one."
    Michelle asked, "Do you like the house?"
    """,
        "question_1": QUESTION_1,
        "question_2": QUESTION_2,
        "question_3": "What had Michelle just bought?",
        "question_4": "Did Samantha know the rug was new?",
        "feedback": "",
    },
    {
        "prompt": """
        All of the class took part in a poetry competition.
    Jane really wanted to win. While she was away, the
    results of the competition were announced: Mary
    was the winner. The next day, Jane bumped into
    Mary. Mary said "How are you feeling?". "Fine
    thanks?" said Jane, "Oh good" said Mary.
    """,
        "question_1": QUESTION_1,
        "question_2": QUESTION_2,
        "question_3": "Who won the story competition?",
        "question_4": "Did Mary know that Jane hadn't heard the results of the competition?",
        "feedback": """
        No, no one said anything they shouldn't have said.  Mary won the story 
    competition.  It is not clear from the story whether Mark knew that Jane hadn't heard the results of the competition
    """,
    },
    {
        "prompt": """
        Alan and Ed were having a drink in a restaurant.
    Alan spilt his coke on the floor by accident. He
    said to Edward "Oh dear, haven't I been clumsy—
    I've spilt my coke!" Edward said "I'll order
    another one."
    """,
        "question_1": QUESTION_1,
        "question_2": QUESTION_2,
        "question_3": "Where did the story take place?",
        "question_4": "Did Alan know Ed was a customer?",
        "feedback": "",
    },
]


def ask_questions(prompt, questions, model, prompt_type, is_chain=False):
    responses = []
    for question in questions:
        full_prompt = prompt + "\n" + question if not is_chain else "only answer for the second story" + question
        response = get_response(URL, full_prompt, model=model)
        responses.append(response)
        logging.info(
            f"\n{prompt_type} Question: {question}\nResponse: {response}\n" + "-" * 50
        )
    return responses


class PromptType(Enum):
    FAUX_PAS = "faux_pas"
    CONTROL = "control"


def log_header(model, description):
    logging.info(f"\nModel: {model} ({description})\n" + "=" * 50)


def log_prompt_section(prompt, prompt_type):
    logging.info("\n" + "-" * 50)
    prompt_type_text = "FAUX PAS" if prompt_type == PromptType.FAUX_PAS else "CONTROL"
    logging.info(f"{prompt_type_text} Prompt: {prompt}")
    logging.info("-" * 50)


def prepare_regular_questions(prompt_set):
    return [prompt_set[f"question_{i}"] for i in range(1, 5) if f"question_{i}" in prompt_set and prompt_set[f"question_{i}"]]


def prepare_restricted_questions(prompt_set):
    return [
        prompt_set.get("question_1", "") + "\n" + QUESTION_1_RESTRICTED,
        prompt_set.get("question_2", "") + "\n" + QUESTION_2_RESTRICTED,
        prompt_set.get("question_3", "") + "\n" + QUESTION_3_RESTRICTED,
        prompt_set.get("question_4", "") + "\n" + QUESTION_4_RESTRICTED,
    ]


def ask_questions_by_type(models, prompts, question_prep_function, description, is_chain=False):
    for model in models:
        log_header(model, description)
        for prompt_set in prompts:
            prompt_type = PromptType.FAUX_PAS if prompt_set in FAUX_PAS_PROMPTS else PromptType.CONTROL
            log_prompt_section(prompt_set['prompt'], prompt_type)
            questions = question_prep_function(prompt_set)
            ask_questions(prompt_set['prompt'], questions, model, prompt_type, is_chain) 



def ask_chain_of_thought_questions(models, faux_pas_prompts, control_prompts):
    prompt_indices = [2, 3]
    for model in models:
        for prompts, prompt_type in [(faux_pas_prompts, PromptType.FAUX_PAS), (control_prompts, PromptType.CONTROL)]:
            for index in prompt_indices:
                if index + 1 < len(prompts):
                    first_prompt_set, second_prompt_set = prompts[index], prompts[index + 1]
                    chain_prompt = f"First Story: {first_prompt_set['prompt']}\n Feedback:{first_prompt_set.get('feedback', '')}\n Second Story:{second_prompt_set['prompt']}"
                    log_header(model, f"Chain-of-Thought with Feedback ({prompt_type.value})")
                    log_prompt_section(chain_prompt, prompt_type)
                    questions = prepare_restricted_questions(second_prompt_set)
                    ask_questions(chain_prompt, questions, model, prompt_type.value, is_chain=True)


def main():
    models = ["dolphin-llama3:70b", "llama3:70b", "mixtral:8x7b"]
    prompts = FAUX_PAS_PROMPTS + CONTROL_PROMPTS

    # Handle regular, restricted, and chain-of-thought questions
    ask_questions_by_type(models, prompts, prepare_regular_questions, "Regular Questions")
    ask_questions_by_type(models, prompts, prepare_restricted_questions, "Restricted Questions")
    ask_chain_of_thought_questions(models, FAUX_PAS_PROMPTS, CONTROL_PROMPTS)


if __name__ == "__main__":
    logging.basicConfig(
        filename="output_log.txt", level=logging.INFO, format="%(message)s"
    )

    start_tunnel(
        remote_server=IMAGINATION_IP,
        ssh_username=SSH_USERNAME,
        ssh_pkey=SSH_KEYFILE,
        remote_port=IMAGINATION_PORT,
        local_port=LOCAL_PORT,
    )

    main()

    stop_tunnel()
