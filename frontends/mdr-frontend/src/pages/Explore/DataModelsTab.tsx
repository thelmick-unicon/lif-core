import DataModelSelector from "../../components/DataModelSelector/DataModelSelector";

const DataModelsTab: React.FC = () => {
  return (
    <DataModelSelector
      dataModeltype="DataModel"
      routPath="/explore/data-models/"
    />
  );
};

export default DataModelsTab;
