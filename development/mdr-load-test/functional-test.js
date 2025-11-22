// API Functional Test Suite
// Comprehensive functional testing of all API endpoints
import http from 'k6/http';
import { check, sleep } from 'k6';
import { config } from './k6.config.js';
import { 
  makeRequest, 
  headers, 
  validatePaginationResponse,
  validateEntityResponse,
  testDataGenerator,
  logTestResult
} from './utils.js';

export let options = {
  stages: [
    { duration: '1m', target: 1 }, // Single user functional testing
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000', 'avg<1000'],
    http_req_failed: ['rate<0.01']
  }
};

export default function () {
  const baseUrl = config.baseUrl;

  // Test all API endpoints systematically
  testHealthEndpoint(baseUrl);
  sleep(1);
  
  testDataModelEndpoints(baseUrl);
  sleep(1);
  
  testEntityEndpoints(baseUrl);
  sleep(1);
  
  testAttributeEndpoints(baseUrl);
  sleep(1);
  
  testValueSetEndpoints(baseUrl);
  sleep(1);
  
  testSearchEndpoints(baseUrl);
  sleep(1);
  
  testTransformationEndpoints(baseUrl);
  sleep(1);
  
  testValueMappingEndpoints(baseUrl);
  sleep(1);
  
  testEntityAssociationEndpoints(baseUrl);
  sleep(1);
  
  testEntityAttributeAssociationEndpoints(baseUrl);
  sleep(1);
  
  testInclusionEndpoints(baseUrl);
  sleep(1);
  
  testDataModelConstraintEndpoints(baseUrl);
  sleep(1);
  
  testValueSetValueEndpoints(baseUrl);
  sleep(2);
}

function testHealthEndpoint(baseUrl) {
  const response = makeRequest(
    http.get,
    `${baseUrl}/health-check`,
    { headers },
    {
      'health check returns 200': (r) => r.status === 200,
      'health check has status': (r) => {
        const body = JSON.parse(r.body);
        return body.hasOwnProperty('status');
      },
      'health check has message': (r) => {
        const body = JSON.parse(r.body);
        return body.hasOwnProperty('message');
      }
    }
  );
  
  logTestResult('Health Check Endpoint', response);
}

function testDataModelEndpoints(baseUrl) {
  // Test GET /datamodels/
  let response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/?pagination=false`,
    { headers },
    {
      'get all data models works': (r) => r.status === 200,
      'data models response has data': (r) => {
        const body = JSON.parse(r.body);
        return body.hasOwnProperty('data') && Array.isArray(body.data);
      }
    }
  );
  logTestResult('GET /datamodels/', response);

  // Test GET /datamodels/ with pagination
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/?page=1&size=10&pagination=true`,
    { headers },
    {
      'paginated data models works': (r) => r.status === 200
    }
  );
  validatePaginationResponse(response);
  logTestResult('GET /datamodels/ (paginated)', response);

  // Test GET /datamodels/ with filters
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/?level_of_access=Public&state=Active&include_extension=true`,
    { headers },
    {
      'filtered data models works': (r) => r.status === 200
    }
  );
  logTestResult('GET /datamodels/ (filtered)', response);

  // Test GET /datamodels/{id}
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/${dataModelId}`,
    { headers },
    {
      'get specific data model works': (r) => r.status === 200 || r.status === 404
    }
  );
  
  if (response.status === 200) {
    validateEntityResponse(response, ['Name', 'DataModelVersion', 'Type']);
  }
  logTestResult(`GET /datamodels/${dataModelId}`, response);

  // Test GET /datamodels/with_details/{id}
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/with_details/${dataModelId}`,
    { headers },
    {
      'get data model with details works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /datamodels/with_details/${dataModelId}`, response);

  // Test GET /datamodels/orglif/
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/orglif/`,
    { headers },
    {
      'get org lif data models works': (r) => r.status === 200
    }
  );
  logTestResult('GET /datamodels/orglif/', response);

  // Test GET /datamodels/open_api_schema/{id}?include_attr_md=true
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodels/open_api_schema/${dataModelId}?include_attr_md=true`,
    { headers },
    {
      'get open api schema works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /datamodels/open_api_schema/${dataModelId}`, response);
}

function testEntityEndpoints(baseUrl) {
  // Test GET /entities/
  let response = makeRequest(
    http.get,
    `${baseUrl}/entities/?pagination=false`,
    { headers },
    {
      'get all entities works': (r) => r.status === 200
    }
  );
  logTestResult('GET /entities/', response);

  // Test GET /entities/ with pagination
  response = makeRequest(
    http.get,
    `${baseUrl}/entities/?page=1&size=10&pagination=true`,
    { headers },
    {
      'paginated entities works': (r) => r.status === 200
    }
  );
  validatePaginationResponse(response);
  logTestResult('GET /entities/ (paginated)', response);

  // Test GET /entities/{id}
  const entityId = testDataGenerator.randomArrayElement(config.testData.entityIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/entities/${entityId}`,
    { headers },
    {
      'get specific entity works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /entities/${entityId}`, response);

  // Test GET /entities/by_data_model_id/{data_model_id}?pagination=false
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/entities/by_data_model_id/${dataModelId}?pagination=false`,
    { headers },
    {
      'get entities by data model works': (r) => r.status === 200
    }
  );
  logTestResult(`GET /entities/by_data_model_id/${dataModelId}`, response);

  // Test GET /entities/entities/by_ids
  const entityIds = config.testData.entityIds.slice(0, 3);
  const idsQueryParams = entityIds.map(id => `ids=${id}`).join('&');
  response = makeRequest(
    http.get,
    `${baseUrl}/entities/entities/by_ids?${idsQueryParams}`,
    { headers },
    {
      'get entities by ids works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /entities/entities/by_ids?${idsQueryParams}`, response);

  // Test GET /entity_associations/by_data_model_id/{data_model_id}?pagination=false&allow_empty=true
  response = makeRequest(
    http.get,
    `${baseUrl}/entity_associations/by_data_model_id/${dataModelId}?pagination=false&allow_empty=true`,
    { headers },
    {
      'get entity associations by data model works': (r) => r.status === 200
    }
  );
  logTestResult(`GET /entity_associations/by_data_model_id/${dataModelId}`, response);

  // Test GET /entity_attribute_associations/by_data_model_id/{data_model_id}?pagination=false
  response = makeRequest(
    http.get,
    `${baseUrl}/entity_attribute_associations/by_data_model_id/${dataModelId}?pagination=false`,
    { headers },
    {
      'get entity attribute associations by data model works': (r) => r.status === 200
    }
  );
  logTestResult(`GET /entity_attribute_associations/by_data_model_id/${dataModelId}`, response);
}

function testAttributeEndpoints(baseUrl) {
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  
  // Test GET /attributes/by_data_model_id/{data_model_id}?pagination=false
  let response = makeRequest(
    http.get,
    `${baseUrl}/attributes/by_data_model_id/${dataModelId}?pagination=false`,
    { headers },
    {
      'get attributes by data model works': (r) => r.status === 200
    }
  );
  logTestResult(`GET /attributes/by_data_model_id/${dataModelId}`, response);
  
  // Test GET /attributes
  response = makeRequest(
    http.get,
    `${baseUrl}/attributes?pagination=false`,
    { headers },
    {
      'get all attributes works': (r) => r.status === 200
    }
  );
  logTestResult('GET /attributes', response);
  
  // Test GET /attributes/by_entity_id/{id}
  const entityId = testDataGenerator.randomArrayElement(config.testData.entityIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/attributes/by_entity_id/${entityId}`,
    { headers },
    {
      'get attributes by entity id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /attributes/by_entity_id/${entityId}`, response);
  
  // Test GET /attributes/{id}
  const attributeId = testDataGenerator.randomArrayElement(config.testData.attributeIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/attributes/${attributeId}`,
    { headers },
    {
      'get specific attribute works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /attributes/${attributeId}`, response);
}

function testValueSetEndpoints(baseUrl) {
  // Test GET /value_sets/
  let response = makeRequest(
    http.get,
    `${baseUrl}/value_sets/?pagination=false`,
    { headers },
    {
      'get all value sets works': (r) => r.status === 200
    }
  );
  logTestResult('GET /value_sets/', response);

  // Test GET /value_sets/ with pagination
  response = makeRequest(
    http.get,
    `${baseUrl}/value_sets/?page=1&size=10&pagination=true`,
    { headers },
    {
      'paginated value sets works': (r) => r.status === 200
    }
  );
  validatePaginationResponse(response);
  logTestResult('GET /value_sets/ (paginated)', response);

  // Test GET /value_sets/{id}
  const valueSetId = testDataGenerator.randomArrayElement(config.testData.valueSetIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/value_sets/${valueSetId}`,
    { headers },
    {
      'get specific value set works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /value_sets/${valueSetId}`, response);

  // Test GET /value_sets/by_data_model_id/{id}
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/value_sets/by_data_model_id/${dataModelId}`,
    { headers },
    {
      'get value sets by data model works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /value_sets/by_data_model_id/${dataModelId}`, response);

  // Test GET /value_sets/usage/{id}
  response = makeRequest(
    http.get,
    `${baseUrl}/value_sets/usage/${valueSetId}`,
    { headers },
    {
      'get value set usage works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /value_sets/usage/${valueSetId}`, response);

  // Test GET /value_sets/{id}/with_values
  response = makeRequest(
    http.get,
    `${baseUrl}/value_sets/${valueSetId}/with_values`,
    { headers },
    {
      'get value set with values works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /value_sets/${valueSetId}/with_values`, response);
}

function testSearchEndpoints(baseUrl) {
  // Test basic search
  let response = makeRequest(
    http.get,
    `${baseUrl}/search/?search_key=name`,
    { headers },
    {
      'basic search works': (r) => r.status === 200,
      'search returns object': (r) => {
        try {
          const body = JSON.parse(r.body);
          return typeof body === 'object';
        } catch (e) {
          return false;
        }
      }
    }
  );
  logTestResult('GET /search/ (basic)', response);

  // Test search with parameters
  response = makeRequest(
    http.get,
    `${baseUrl}/search/?search_key=entity&only_extension=true&only_base=false`,
    { headers },
    {
      'parameterized search works': (r) => r.status === 200
    }
  );
  logTestResult('GET /search/ (with parameters)', response);

  // Test search with data model filter
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/search/?search_key=attribute&data_model_id=${dataModelId}`,
    { headers },
    {
      'filtered search works': (r) => r.status === 200
    }
  );
  logTestResult('GET /search/ (filtered)', response);
}

function testTransformationEndpoints(baseUrl) {
  // Test GET /transformation_groups/?pagination=false
  let response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/?pagination=false`,
    { headers },
    {
      'get transformation groups works': (r) => r.status === 200
    }
  );
  logTestResult('GET /transformation_groups/', response);

  // Test GET /transformation_groups/data_models/
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/data_models/`,
    { headers },
    {
      'get transformation groups data models works': (r) => r.status === 200
    }
  );
  logTestResult('GET /transformation_groups/data_models/', response);

  // Test GET /transformation_groups/{id}
  const transformationGroupId = testDataGenerator.randomArrayElement(config.testData.transformationGroupIds || [1, 2, 3, 4, 5]);
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/${transformationGroupId}`,
    { headers },
    {
      'get specific transformation group works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /transformation_groups/${transformationGroupId}`, response);

  // Test GET /transformation_groups/exists/by-triplet
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/exists/by-triplet?sourceId=1&targetId=17&version=1.0`,
    { headers },
    {
      'get transformation groups exists by triplet works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult('GET /transformation_groups/exists/by-triplet', response);

  // Test GET /transformation_groups/{id}/source_and_target
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/${transformationGroupId}/source_and_target`,
    { headers },
    {
      'get transformation groups source and target works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /transformation_groups/${transformationGroupId}/source_and_target`, response);

  // Test GET /transformation_groups/{id}/transformations
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/${transformationGroupId}/transformations`,
    { headers },
    {
      'get transformation groups transformations works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /transformation_groups/${transformationGroupId}/transformations`, response);

  // Test GET /transformation_groups/transformations/{id}
  const transformationId = testDataGenerator.randomArrayElement(config.testData.transformationIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/transformations/${transformationId}`,
    { headers },
    {
      'get specific transformation works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /transformation_groups/transformations/${transformationId}`, response);

  // Test GET /transformation_groups/{id}/transformations_by_path_ids
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/${transformationGroupId}/transformations_by_path_ids?path_ids=1,2,3`,
    { headers },
    {
      'get transformations by path ids works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /transformation_groups/${transformationGroupId}/transformations_by_path_ids`, response);

  // Test GET /transformation_groups/transformations_for_data_models/
  response = makeRequest(
    http.get,
    `${baseUrl}/transformation_groups/transformations_for_data_models/?source_data_model_id=26&target_data_model_id=17&size=100`,
    { headers },
    {
      'get transformations for data models works': (r) => r.status === 200
    }
  );
  logTestResult('GET /transformation_groups/transformations_for_data_models/', response);

  // Test GET /transformations_by_path_ids
  response = makeRequest(
    http.get,
    `${baseUrl}/transformations_by_path_ids?path_ids=1,2,3`,
    { headers },
    {
      'get transformations by path ids works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult('GET /transformations_by_path_ids', response);

  // Test GET /transformations_for_data_models
  response = makeRequest(
    http.get,
    `${baseUrl}/transformations_for_data_models?source_data_model_id=1&target_data_model_id=17`,
    { headers },
    {
      'get transformations for data models works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult('GET /transformations_for_data_models', response);
}

function testValueMappingEndpoints(baseUrl) {
  // Test GET /value_mappings/
  let response = makeRequest(
    http.get,
    `${baseUrl}/value_mappings/?page=1&size=10`,
    { headers },
    {
      'get value mappings works': (r) => r.status === 200
    }
  );
  validatePaginationResponse(response);
  logTestResult('GET /value_mappings/', response);

  // Test GET /value_mappings/{id}
  const valueMappingId = testDataGenerator.randomArrayElement(config.testData.valueMappingIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/value_mappings/${valueMappingId}`,
    { headers },
    {
      'get specific value mapping works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /value_mappings/${valueMappingId}`, response);

  // Test GET /value_mappings/by_transformation_group/{id}
  const transformationGroupId = testDataGenerator.randomArrayElement(config.testData.transformationGroupIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/value_mappings/by_transformation_group/${transformationGroupId}`,
    { headers },
    {
      'get value mappings by transformation group works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /value_mappings/by_transformation_group/${transformationGroupId}`, response);

  // NOTE: The following endpoints appear to have routing conflicts with /value_mappings/{id}
  // TODO: Verify correct endpoint structure with API documentation
  
  // Test GET /value_mappings/by_value_ids
  // const valueIds = config.testData.valueIds.slice(0, 3);
  // const valueIdsQueryParams = valueIds.map(id => `value_ids=${id}`).join('&');
  // response = makeRequest(
  //   http.get,
  //   `${baseUrl}/value_mappings/by_value_ids?${valueIdsQueryParams}`,
  //   { headers },
  //   {
  //     'get value mappings by value ids works': (r) => r.status === 200 || r.status === 404
  //   }
  // );
  // logTestResult(`GET /value_mappings/by_value_ids?${valueIdsQueryParams}`, response);

  // Test GET /value_mappings/by_value_set_ids
  // const valueSetIds = config.testData.valueSetIds.slice(0, 3);
  // const valueSetIdsQueryParams = valueSetIds.map(id => `value_set_ids=${id}`).join('&');
  // response = makeRequest(
  //   http.get,
  //   `${baseUrl}/value_mappings/by_value_set_ids?${valueSetIdsQueryParams}`,
  //   { headers },
  //   {
  //     'get value mappings by value set ids works': (r) => r.status === 200 || r.status === 404
  //   }
  // );
  // logTestResult(`GET /value_mappings/by_value_set_ids?${valueSetIdsQueryParams}`, response);
}

function testEntityAssociationEndpoints(baseUrl) {
  // NOTE: GET /entity_associations appears to not be supported (405 Method Not Allowed)
  // Commenting out until API endpoint structure is clarified
  
  // Test GET /entity_associations
  // let response = makeRequest(
  //   http.get,
  //   `${baseUrl}/entity_associations?pagination=false`,
  //   { headers },
  //   {
  //     'get all entity associations works': (r) => r.status === 200
  //   }
  // );
  // logTestResult('GET /entity_associations', response);

  // Test GET /entity_associations/{id}
  const entityAssociationId = testDataGenerator.randomArrayElement(config.testData.entityAssociationIds);
  let response = makeRequest(
    http.get,
    `${baseUrl}/entity_associations/${entityAssociationId}`,
    { headers },
    {
      'get specific entity association works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /entity_associations/${entityAssociationId}`, response);

  // Test GET /entity_associations/by_parent_entity_id/{id}
  const entityId = testDataGenerator.randomArrayElement(config.testData.entityIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/entity_associations/by_parent_entity_id/${entityId}`,
    { headers },
    {
      'get entity associations by parent entity id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /entity_associations/by_parent_entity_id/${entityId}`, response);
}

function testEntityAttributeAssociationEndpoints(baseUrl) {
  // NOTE: GET /entity_attribute_associations appears to not be supported (405 Method Not Allowed)
  // Commenting out until API endpoint structure is clarified
  
  // Test GET /entity_attribute_associations
  // let response = makeRequest(
  //   http.get,
  //   `${baseUrl}/entity_attribute_associations?pagination=false`,
  //   { headers },
  //   {
  //     'get all entity attribute associations works': (r) => r.status === 200
  //   }
  // );
  // logTestResult('GET /entity_attribute_associations', response);

  // Test GET /entity_attribute_associations/{id}
  const entityAttributeAssociationId = testDataGenerator.randomArrayElement(config.testData.entityAttributeAssociationIds);
  let response = makeRequest(
    http.get,
    `${baseUrl}/entity_attribute_associations/${entityAttributeAssociationId}`,
    { headers },
    {
      'get specific entity attribute association works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /entity_attribute_associations/${entityAttributeAssociationId}`, response);

  // Test GET /entity_attribute_associations/by_entity_id/{id}
  const entityId = testDataGenerator.randomArrayElement(config.testData.entityIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/entity_attribute_associations/by_entity_id/${entityId}`,
    { headers },
    {
      'get entity attribute associations by entity id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /entity_attribute_associations/by_entity_id/${entityId}`, response);

  // Test GET /entity_attribute_associations/by_attribute_id/{id}
  const attributeId = testDataGenerator.randomArrayElement(config.testData.attributeIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/entity_attribute_associations/by_attribute_id/${attributeId}`,
    { headers },
    {
      'get entity attribute associations by attribute id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /entity_attribute_associations/by_attribute_id/${attributeId}`, response);
}

function testInclusionEndpoints(baseUrl) {
  // NOTE: GET /inclusions appears to not be supported (405 Method Not Allowed)
  // Commenting out until API endpoint structure is clarified
  
  // Test GET /inclusions
  // let response = makeRequest(
  //   http.get,
  //   `${baseUrl}/inclusions?pagination=false`,
  //   { headers },
  //   {
  //     'get all inclusions works': (r) => r.status === 200
  //   }
  // );
  // logTestResult('GET /inclusions', response);

  // Test GET /inclusions/{id}
  const inclusionId = testDataGenerator.randomArrayElement(config.testData.inclusionIds);
  let response = makeRequest(
    http.get,
    `${baseUrl}/inclusions/${inclusionId}`,
    { headers },
    {
      'get specific inclusion works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /inclusions/${inclusionId}`, response);

  // Test GET /inclusions/by_data_model_id/{id}
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/inclusions/by_data_model_id/${dataModelId}`,
    { headers },
    {
      'get inclusions by data model id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /inclusions/by_data_model_id/${dataModelId}`, response);

  // Test GET /inclusions/entities/by_data_model_id/{id}
  response = makeRequest(
    http.get,
    `${baseUrl}/inclusions/entities/by_data_model_id/${dataModelId}`,
    { headers },
    {
      'get inclusion entities by data model id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /inclusions/entities/by_data_model_id/${dataModelId}`, response);

  // Test GET /inclusions/attributes/by_data_model_id/{id}
  response = makeRequest(
    http.get,
    `${baseUrl}/inclusions/attributes/by_data_model_id/${dataModelId}`,
    { headers },
    {
      'get inclusion attributes by data model id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /inclusions/attributes/by_data_model_id/${dataModelId}`, response);

  // Test GET /inclusions/attributes/by_data_model_id/{id}/by_entity_id/{id}
  const entityId = testDataGenerator.randomArrayElement(config.testData.entityIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/inclusions/attributes/by_data_model_id/${dataModelId}/by_entity_id/${entityId}`,
    { headers },
    {
      'get inclusion attributes by data model and entity id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /inclusions/attributes/by_data_model_id/${dataModelId}/by_entity_id/${entityId}`, response);
}

function testDataModelConstraintEndpoints(baseUrl) {
  // Test GET /datamodel_constraints
  let response = makeRequest(
    http.get,
    `${baseUrl}/datamodel_constraints?pagination=false`,
    { headers },
    {
      'get all datamodel constraints works': (r) => r.status === 200
    }
  );
  logTestResult('GET /datamodel_constraints', response);

  // Test GET /datamodel_constraints/{id}
  const dataModelConstraintId = testDataGenerator.randomArrayElement(config.testData.dataModelConstraintIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodel_constraints/${dataModelConstraintId}`,
    { headers },
    {
      'get specific datamodel constraint works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /datamodel_constraints/${dataModelConstraintId}`, response);

  // Test GET /datamodel_constraints/by_data_model_id/{id}
  const dataModelId = testDataGenerator.randomArrayElement(config.testData.modelIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/datamodel_constraints/by_data_model_id/${dataModelId}`,
    { headers },
    {
      'get datamodel constraints by data model id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /datamodel_constraints/by_data_model_id/${dataModelId}`, response);
}

function testValueSetValueEndpoints(baseUrl) {
  // Test GET /value_set_values
  let response = makeRequest(
    http.get,
    `${baseUrl}/value_set_values?pagination=false`,
    { headers },
    {
      'get all value set values works': (r) => r.status === 200
    }
  );
  logTestResult('GET /value_set_values', response);

  // Test GET /value_set_values/{id}
  const valueSetValueId = testDataGenerator.randomArrayElement(config.testData.valueSetValueIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/value_set_values/${valueSetValueId}`,
    { headers },
    {
      'get specific value set value works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /value_set_values/${valueSetValueId}`, response);

  // Test GET /value_set_values/by_valueset_id/{id}
  const valueSetId = testDataGenerator.randomArrayElement(config.testData.valueSetIds);
  response = makeRequest(
    http.get,
    `${baseUrl}/value_set_values/by_valueset_id/${valueSetId}`,
    { headers },
    {
      'get value set values by valueset id works': (r) => r.status === 200 || r.status === 404
    }
  );
  logTestResult(`GET /value_set_values/by_valueset_id/${valueSetId}`, response);
}

export function teardown() {
  console.log('Functional test completed');
}