from flask import Blueprint, request, jsonify, render_template, redirect, \
    url_for
from .professor_model import Professor

professor_blueprint = Blueprint('professores', __name__)


@professor_blueprint.route('/professores/criar_professor',
                           methods=['GET', 'POST'])
def criar_professor():
    if request.method == 'POST':
        data = request.form
        Professor.create_professor(data)
        return redirect(url_for('professores.listar_professores'))
    return render_template('criar_professor.html')


@professor_blueprint.route(
    '/professores/atualizar_professor/<int:professor_id>',
    methods=['GET', 'POST'])
def atualizar_professor(professor_id):
    professor = Professor.get_professor(professor_id)
    if request.method == 'POST':
        data = request.form
        if not professor:
            return jsonify({'message': 'Professor não encontrado'}), 404
        Professor.update_professor(professor_id, data)
        return redirect(url_for('professores.listar_professores'))
    return render_template('atualizar_professor.html', professor=professor)


@professor_blueprint.route(
    '/professores/excluir_professor/<int:professor_id>',
    methods=['POST'])
def excluir_professor(professor_id):
    if not Professor.delete_professor(professor_id):
        return jsonify({'message': 'Professor não encontrado'}), 404
    return redirect(url_for('professores.listar_professores'))


@professor_blueprint.route('/professores/listar_professor', methods=['GET'])
def listar_professores():
    professores = Professor.get_all_professores()
    return render_template('listar_professores.html', professores=professores)


@professor_blueprint.route('/professores', methods=['GET'])
def get_professores():
    professores = Professor.get_all_professores()
    return jsonify([professor.to_dict() for professor in professores])


@professor_blueprint.route('/professores', methods=['POST'])
def create_professor():
    data = request.json
    novo_professor = Professor.create_professor(data)
    return jsonify(novo_professor.to_dict()), 201


@professor_blueprint.route('/professores/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
    data = request.json
    professor = Professor.update_professor(professor_id, data)
    if not professor:
        return jsonify({'message': 'Professor não encontrado'}), 404
    return jsonify(professor.to_dict()), 200


@professor_blueprint.route('/professores/<int:professor_id>',
                           methods=['DELETE'])
def delete_professor(professor_id):
    if not Professor.delete_professor(professor_id):
        return jsonify({'message': 'Professor não encontrado'}), 404
    return jsonify({'message': 'Professor excluído com sucesso'}), 204
