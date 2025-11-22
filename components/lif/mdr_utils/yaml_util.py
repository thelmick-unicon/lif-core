import yaml
from lif.mdr_utils.error_handling import build_exception, generate_unique_error_id, log_error_template
from lif.mdr_utils.logger_config import get_logger
from http import HTTPStatus

logger = get_logger(__name__)


def load_conf_file(config_file):
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
        # logger.info("Yaml Config: %s", config)
    #    adapters_conf = config[0]["adapters"]
    return config


async def get_sql_config_data(section, key):
    logger.info("In get data method. section :  %s, key: %s", section, key)
    try:
        db_sqls = load_conf_file("/usr/src/service/config_files/sql_config.yaml")
        is_parameter_order = False
        for sqls in db_sqls[section]:
            if sqls["name"] == key:
                if "parameter_order" in sqls:
                    is_parameter_order = True
                if "sqls" in sqls:
                    if is_parameter_order:
                        return sqls["sqls"], sqls["parameter_order"]
                    return sqls["sqls"], None
                if is_parameter_order:
                    return sqls["sql"], sqls["parameter_order"]
                return sqls["sql"], None

        # In case of we do not find resource(key) into our sql_config.yaml file.
        error_id = generate_unique_error_id()
        logger.error(log_error_template(), error_id, f"Could not find provided resource : {key} in sql_config.yaml")
        raise build_exception(
            error_id, f"Could not find provided resource : {key} in sql config file", HTTPStatus.BAD_REQUEST
        )
    except BaseException as e:
        error_id = generate_unique_error_id()
        logger.error(
            log_error_template(), error_id, f"Error while getting config from sql_config.yaml file. Error  : {e}"
        )
        raise build_exception(
            error_id, f"Error while getting SQL config. Error  : {e}", HTTPStatus.INTERNAL_SERVER_ERROR
        )
