import yaml
from fastapi import APIRouter, Depends, Response
from jinja2 import Template
from lif.mdr_services import jinja_translation_service
from lif.mdr_utils.database_setup import get_session
from lif.mdr_utils.logger_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = get_logger(__name__)


@router.get("/")
async def get_jinja_translation(
    source_data_model_name: str,
    source_data_model_version: str,
    target_data_model_name: str,
    target_data_model_version: str,
    session: AsyncSession = Depends(get_session),
):
    jinja_data = await jinja_translation_service.generate_jinja(
        session=session,
        source_data_model_name=source_data_model_name,
        source_data_model_version=source_data_model_version,
        target_data_model_name=target_data_model_name,
        target_data_model_version=target_data_model_version,
    )

    # Convert data to YAML format
    # Define a custom Dumper to handle multiline strings
    class MyDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):  # cspell:disable-line
            return super(MyDumper, self).increase_indent(flow, False)

        def represent_scalar(self, tag, value, style=None):
            if tag == "tag:yaml.org,2002:str" and "\n" in value:
                style = "|"
                logger.info(f"style : {style}")
            return super(MyDumper, self).represent_scalar(tag, value, style)

    yaml_data = yaml.dump(
        jinja_data,
        Dumper=MyDumper,
        default_flow_style=False,  # Enable block style (pretty printing)
        sort_keys=False,
    )

    template = Template(yaml_data)
    rendered_yaml = template.render()
    # Return response with YAML content type
    return Response(content=rendered_yaml, media_type="application/x-yaml")
