import { Badge, Card, DataList } from "@radix-ui/themes";
import "./ObjectDetails.css";

interface ObjectDetailsProps {
  object: Record<string, any> | null | undefined;
  orient?: any;
  card?: boolean;
  excludeKeys?: string[];
}

const ObjectDetails: React.FC<ObjectDetailsProps> = ({
  object,
  orient = "horizontal",
  card = true,
  excludeKeys = ["Deleted"],
}) => {
  if (!object) return null;

  const entries = Object.entries(object).filter(
    ([key]) => !excludeKeys.includes(key)
  );
  // console.log("entries :>> ", entries);

  return (
    card ? (
      <Card className="details-grid">
        <DataList.Root orientation={{ initial: "vertical", sm: "horizontal" }}>
          {entries.map(([key, value]) => {
            return (
              <DataList.Item key={key}>
                <DataList.Label minWidth="88px">{key}</DataList.Label>
                <DataList.Value>{!value ? ( "—" ) : ( <span className="value-text">{typeof value === "boolean" ? (<i>true</i>) : value}</span> )}</DataList.Value>
              </DataList.Item>
            );
          })}
        </DataList.Root>
      </Card>
    ) : (
      <DataList.Root orientation={orient}>
        {entries.map(([key, value]) => {
          return (
            <DataList.Item key={key}>
              <DataList.Label minWidth="88px">{key}</DataList.Label>
              <DataList.Value>{!value ? ( "—" ) : ( <span className="value-text">{typeof value === "boolean" ? (<i>true</i>) : value}</span> )}</DataList.Value>
            </DataList.Item>
          );
        })}
      </DataList.Root>
    )
  );
};

export default ObjectDetails;
