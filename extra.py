from flask import Blueprint

# بنعمل وحدة جديدة مستقلة للأشياء الجديدة
extra_bp = Blueprint('extra', __name__)

@extra_bp.route('/asmra-extra')
def extra_page():
    return "<h1>🚀 مبروك يا أبو سمرة! الصفحة الإضافية الجديدة اشتغلت بنجاح من الملف المنفصل!</h1>"
