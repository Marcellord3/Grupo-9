from config import db


class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey(
        'professor.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'professor_id': self.professor_id,
            'ativo': self.ativo
        }

    @classmethod
    def create_turma(cls, data):
        nova_turma = cls(
            descricao=data['descricao'],
            professor_id=data['professor_id'],
            ativo=data.get('ativo', True)
        )
        db.session.add(nova_turma)
        db.session.commit()
        return nova_turma

    @classmethod
    def get_turma(cls, turma_id):
        return cls.query.get(turma_id)

    @classmethod
    def get_all_turmas(cls):
        return cls.query.all()

    @classmethod
    def update_turma(cls, turma_id, data):
        turma = cls.query.get(turma_id)
        if not turma:
            return None
        turma.descricao = data.get('descricao', turma.descricao)
        turma.professor_id = data.get('professor_id', turma.professor_id)
        turma.ativo = data.get('ativo', turma.ativo)
        db.session.commit()
        return turma

    @classmethod
    def delete_turma(cls, turma_id):
        turma = cls.query.get(turma_id)
        if not turma:
            return None
        db.session.delete(turma)
        db.session.commit()
        return True
