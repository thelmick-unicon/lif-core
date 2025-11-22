import DataModelSelector from "../../components/DataModelSelector/DataModelSelector";
const DataModels: React.FC = () => {
  return (
    <DataModelSelector
      dataModeltype="DataModel"
      routPath="/explore/data-models/"
    />
  );
};

export default DataModels;
