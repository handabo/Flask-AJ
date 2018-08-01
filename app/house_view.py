
import os
from flask import Blueprint, render_template, session, jsonify, request

from app.models import User, Area, House, HouseImage, Facility
from utils import status_code
from utils.functions import is_login
from utils.settings import upload_folder


# 实例化house蓝图
house_blueprint = Blueprint('house', __name__)


# 进入我的房源页面
@house_blueprint.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')


# 验证是否实名认证, 如果实名认证成功展示房源信息
@house_blueprint.route('/house_info/', methods=['GET'])
@is_login
def house_info():
    user = User.query.get(session['user_id'])
    if user.id_card:
        # 实名认证成功
        # TODO：返回用户添加的房屋信息
        houses = House.query.filter(House.user_id == session['user_id'])
        houses_list = [house.to_dict() for house in houses]
        return jsonify(code=status_code.OK, houses_list=houses_list)
    else:
        return jsonify(status_code.HOUSE_USER_INFO_ID_CARD_INVALID)


# 进入发布新房源页面
@house_blueprint.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


# 获取房源配套设施
@house_blueprint.route('/area_facility/', methods=['GET'])
def area_facility():
    areas = Area.query.all()
    facilitys = Facility.query.all()

    areas_json = [area.to_dict() for area in areas]
    facilitys_json = [facility.to_dict() for facility in facilitys ]

    return jsonify(code=status_code.OK, areas=areas_json, facilitys=facilitys_json)


# 发布新房源(创建房屋信息)
@house_blueprint.route('/newhouse/', methods=['POST'])
def my_newhouse():
    house_dict = request.form                       # 保存房屋信息, 设施信息

    house = House()
    house.user_id = session['user_id']              # 获取用户id
    house.title = house_dict.get('title')           # 房屋标题
    house.price = house_dict.get('price')           # 每晚价格
    house.area_id = house_dict.get('area_id')       # 所在城区
    house.address = house_dict.get('address')       # 详细地址
    house.room_count = house_dict.get('room_count') # 出租房间数目
    house.acreage = house_dict.get('acreage')       # 房屋面积
    house.unit = house_dict.get('unit')             # 户型描述
    house.capacity = house_dict.get('capacity')     # 宜住人数
    house.beds = house_dict.get('beds')             # 卧床配置
    house.deposit = house_dict.get('deposit')       # 押金数额
    house.min_days = house_dict.get('min_days')     # 最少入住天数
    house.max_days = house_dict.get('max_days')     # 最多入住天数

    facilitys = house_dict.getlist('facility')
    for facility_id in facilitys:
        facility = Facility.query.get(facility_id)
        # 多对多关联
        house.facilities.append(facility)
    house.add_update()
    return jsonify(code=status_code.OK, house_id=house.id)


# 创建房屋图片
@house_blueprint.route('/house_images/', methods=['POST'])
def houseimages():
    # 创建房屋图片
    house_id = request.form.get('house_id')
    image = request.files.get('house_image')
    # 保存图片路径  static/media/upload/xxx.jpg
    save_url = os.path.join(upload_folder, image.filename)
    image.save(save_url)
    # 保存房屋图片信息
    house_image = HouseImage()
    house_image.house_id = house_id
    image_url = os.path.join('upload', image.filename)
    house_image.url = image_url
    house_image.add_update()

    # 创建房屋主图
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = image_url
        house.add_update()
    return jsonify(code=status_code.OK, image_url=image_url)


# 进入房间详情页面
@house_blueprint.route('/detail/', methods=['GET'])
def house_detail():
    return render_template('detail.html')


# 展示房间详细信息
@house_blueprint.route('/house_detail/<int:id>/', methods=['GET'])
def houses_detail(id):
    house = House.query.get(id)
    return jsonify(code=status_code.OK, house=house.to_full_dict())













