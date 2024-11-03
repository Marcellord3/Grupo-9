from config import db


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.String(250))

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacoes': self.observacoes
        }

    @classmethod
    def get_all_professores(cls):
        return cls.query.all()

    @classmethod
    def create_professor(cls, data):
        novo_professor = cls(
            nome=data['nome'],
            idade=data['idade'],
            materia=data['materia'],
            observacoes=data.get('observacoes')
        )
        db.session.add(novo_professor)
        db.session.commit()
        return novo_professor

    @classmethod
    def update_professor(cls, professor_id, data):
        professor = cls.query.get(professor_id)
        if not professor:
            return None
        professor.nome = data.get('nome', professor.nome)
        professor.idade = data.get('idade', professor.idade)
        professor.materia = data.get('materia', professor.materia)
        professor.observacoes = data.get('observacoes', professor.observacoes)
        db.session.commit()
        return professor

    @classmethod
    def delete_professor(cls, professor_id):
        professor = cls.query.get(professor_id)
        if not professor:
            return None
        db.session.delete(professor)
        db.session.commit()
        return True
