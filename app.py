import json
from flask import Flask, request, render_template, redirect, url_for, abort

app = Flask(__name__)


def get_level():
    try:
        with open('save.dat', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        abort(404, description="请检查 ./save.dat 是否缺失或内容是否为整数，该文件为存档文件，确定当前关卡数")


def load_level_data(level):
    try:
        with open(f'./static/level-{level}/data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        abort(400,
              description=f"请检查 ./static/level-{level}/data.json 文件是否缺失或是否为正确的 json 文件，该文件为题目的说明文件")


@app.route('/')
def index():
    level = get_level()
    return redirect(url_for("level", level=level))


@app.route('/level/<int:level>')
def level(level):
    level_data = load_level_data(level)

    title = level_data.get('title', '标题缺失')
    description = level_data.get('description', '说明缺失')
    flag = level_data.get('flag', '')
    src = f'../static/level-{level}/challenge.zip'

    return render_template(['template.html'], title=title, description=description, src=src, flag=flag)


@app.route('/submit', methods=['POST'])
def submit_form():
    tmp_flag = request.form.get('flag')
    level = get_level()

    level_data = load_level_data(level)
    correct_flag = level_data.get('flag', '')

    if tmp_flag == correct_flag:
        with open('save.dat', 'w', encoding='utf-8') as f:
            f.write(f'{level + 1}')
        return redirect(url_for('level', level=level + 1))
    else:
        return "flag 错误", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
