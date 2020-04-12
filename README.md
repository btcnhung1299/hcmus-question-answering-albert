# Question Answering with Albert

In this project, we build a close-domain English question answering system and create a RESTful API whose response is an answer for a question given a passage. The current version has been tested locally.

The main architeture relies on [Albert](https://arxiv.org/abs/1909.11942), a novel model based on the revolutionary BERT by Google. We use the re-implementation of [Huggingface](https://github.com/huggingface/transformers) for training and achieve 88.30 F1 and 80.76 EM on SQuAD 1.1 dev set.

You can find materials to re-produce the results here: [training script](https://colab.research.google.com/drive/1lQ8tjqc5lNvykKqXd9ULVqd7abPbZBjZ), [archived weights](https://drive.google.com/file/d/1sIU-x4J2LJlC1Jh5MRW2bUaAq0d8HX8c/view?usp=sharing).

To start a server locally, please go under `hcmus-answering-answering-albert` (clone this repo) and enter this snippet:

```console
flask run
```

**Format of request:**
```json
{
    "context": "Revision week refers to a period in the UK and other Commonwealth countries preceding examinations in high schools, higher education institutions, and military colleges. In American colleges, this period is known as a Reading Period. Generally, this period is one week long and free of classes or assessment, permitting students to spend the period revising material, generally in preparation for final exams. It is not often allocated for mid-semester or ongoing assessment. Each day of such a period may be referred to as a reading day.",
    "question": "How long is revision week?"
}
```

Expected response:
```json
{
    "answer": "one week"
}
```

We completed this project as a coursework in Natural Language Processing ([slide](https://docs.google.com/presentation/d/1aIP1sQawqy9HKeNGlpj7A4wRrMlP3VT2dbzAjGZZEzc/edit?usp=sharing)).
If you have any questions regarding this project, please reach out for me at btcnhung.1299@gmail.com.
