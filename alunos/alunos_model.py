from config import db
from datetime import datetime, date
from turma.turma_model import Turma


class AlunoNaoEncontrado(Exception):
    pass


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float)

    def calcular_idade(self):
        today = date.today()
        idade = today.year - self.data_nascimento.year - \
            ((today.month, today.day) <
             (self.data_nascimento.month, self.data_nascimento.day))
        return idade

    def calcular_media_final(self):
        if (self.nota_primeiro_semestre is None or
                self.nota_segundo_semestre is None):
            return None
        return (self.nota_primeiro_semestre +
                self.nota_segundo_semestre) / 2

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'turma_id': self.turma_id,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),
            'idade': self.calcular_idade(),
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre
        }


class AlunoService:
    @staticmethod
    def aluno_por_id(id_aluno):
        aluno = Aluno.query.get(id_aluno)
        if not aluno:
            raise AlunoNaoEncontrado("Aluno não encontrado")
        return aluno

    @staticmethod
    def listar_alunos():
        return Aluno.query.all()

    @staticmethod
    def adicionar_aluno(aluno_data):
        turma_existente = Turma.query.get(aluno_data['turma_id'])
        if not turma_existente:
            print("Turma não encontrada.")
            return None
        novo_aluno = Aluno(
            nome=aluno_data['nome'],
            turma_id=aluno_data['turma_id'],
            data_nascimento=datetime.strptime(
                aluno_data['data_nascimento'], '%d/%m/%Y').date(),
            nota_primeiro_semestre=aluno_data['nota_primeiro_semestre'],
            nota_segundo_semestre=aluno_data['nota_segundo_semestre']
        )
        db.session.add(novo_aluno)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return novo_aluno

    @staticmethod
    def atualizar_aluno(id_aluno, novos_dados):
        aluno = Aluno.query.get(id_aluno)
        if not aluno:
            raise AlunoNaoEncontrado("Aluno não encontrado")
        for chave, valor in novos_dados.items():
            if chave == 'data_nascimento':
                aluno.data_nascimento = datetime.strptime(
                    valor, '%d/%m/%Y').date()
            else:
                setattr(aluno, chave, valor)
        db.session.commit()
        return aluno

    @staticmethod
    def excluir_aluno(id_aluno):
        aluno = Aluno.query.get(id_aluno)
        if not aluno:
            raise AlunoNaoEncontrado("Aluno não encontrado")
        db.session.delete(aluno)
        db.session.commit()
