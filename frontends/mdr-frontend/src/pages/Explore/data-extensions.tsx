import DataModelSelector from "../../components/DataModelSelector/DataModelSelector";

const DataExtensions: React.FC = () => {
  return (
    <DataModelSelector
      // listTitle="Organization's LIF"
      dataModeltype="OrgLIF"
      routPath="/explore/data-extensions/"
    />
  );
};

export default DataExtensions;
