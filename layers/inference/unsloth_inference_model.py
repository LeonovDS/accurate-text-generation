from layers.inference.inference_model import InferenceModel


class UnslothInferenceModel(InferenceModel):
    def __init__(self, model_name: str, output_tokens: int = 512, load_in_4bit: bool = True):
        self.__model_name = model_name
        self.__model = None
        self.__tokenizer = None
        self.__output_tokens = output_tokens
        self.__load_in_4bit = load_in_4bit

    def _on_enter(self):
        from unsloth import FastLanguageModel
        self.__model, self.__tokenizer = FastLanguageModel.from_pretrained(
            model_name=self.__model_name,
            load_in_4bit=self.__load_in_4bit,
        )
        FastLanguageModel.for_inference(self.__model)

    def _on_exit(self):
        if self.__model is not None:
            del self.__model
        if self.__tokenizer is not None:
            del self.__tokenizer

    def generate(self, prompt: str) -> str:
        tokens = self.__tokenizer([prompt], return_tensors="pt").to("cuda")
        outputs = self.__model.generate(**tokens, max_new_tokens=self.__output_tokens, use_cache=True)
        return self.__tokenizer.batch_decode(outputs)
