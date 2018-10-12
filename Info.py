# 全局变量
class Info:
    # 自动保存间隔时间
    AUTO_SAVE_TIME: int = 3000000
    # 输入输出设备
    INPUT_DEVICE_INFO: dict = {}
    OUTPUT_DEVICE_INFO: dict = {}

    # 特征值-控件对象
    VALUE_WIDGET: dict = {}

    WIDGET_INFO: dict = {}

    # 当前导入导出文件名
    FILE_NAME: str = ""

    # 对widget计数
    WIDGET_COUNT: dict = {
        "TIMELINE_COUNT": 0,
        # event
        "CYCLE_COUNT": 0,
        "SOUNTOUT_COUNT": 0,
        "TEXT_COUNT": 0,
        "IMAGE_COUNT": 0,
        "VIDEO_COUNT": 0,
        # eye tracker
        "OPEN_COUNT": 0,
        "DC_COUNT": 0,
        "CALIBRATION_COUNT": 0,
        "ACTION_COUNT": 0,
        "STARTR_COUNT": 0,
        "ENDR_COUNT": 0,
        "CLOSE_COUNT": 0,
        # quest
        "QUESTINIT_COUNT": 0,
        "QUESTUPDATA_COUNT": 0,
        "QUESTGETVALUE_COUNT": 0,
        # condition
        "IF_ELSE_COUNT": 0,
        "SWITCH_COUNT": 0,
        "OTHER_COUNT": 0
    }
