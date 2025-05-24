class BasePromptTemplate:
    """基于 Pydantic 的基础提示模板类。"""
    
    template: str
    def __init__(self,template: str):
        self.template = template
    

    @classmethod
    def from_template(cls, template: str, **kwargs):
        """从字符串模板创建实例。允许子类传递额外参数。"""
        return cls(template=template, **kwargs)

    def format(self, **kwargs) -> str:
        """
        格式化模板。子类应覆盖此方法以实现具体的格式化逻辑。
        默认实现使用 str.format。
        """
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(
                f"Missing key '{e}' in format arguments for template: {self.template}"
            )