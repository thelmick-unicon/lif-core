import "./lif-model.css";
import DataModelSelector from "../../components/DataModelSelector/DataModelSelector";

const LifModel: React.FC = () => {
  return (
    <DataModelSelector
      // sidebar={<ObjectDetails object={modelDetails} />}
      dataModeltype="LIF"
      routPath="/explore/lif-model/"
    />
  );
};

export default LifModel;
