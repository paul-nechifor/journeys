import { useState, useLayoutEffect } from "react";
import * as am5 from "@amcharts/amcharts5";
import * as am5hierarchy from "@amcharts/amcharts5/hierarchy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

import Button from "@mui/material/Button";
import DownloadIcon from "@mui/icons-material/Download";
import CircularProgress from "@mui/material/CircularProgress";

export default function App() {
  const [data, setData] = useState<null | unknown[]>(null);
  const [isLoading, setIsLoading] = useState(false);
  return (
    <div>
      {!!data ? (
        <Chart data={data} />
      ) : (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100vh",
          }}
        >
          {isLoading ? (
            <CircularProgress />
          ) : (
            <Button
              variant="contained"
              onClick={async () => {
                setIsLoading(true);
                const response = await fetch(
                  "http://localhost:8000/get-journeys",
                );
                const { data } = await response.json();
                addHtmlRepresentation(data);
                setIsLoading(false);
                setData([data]);
              }}
              startIcon={<DownloadIcon />}
            >
              Load Journeys
            </Button>
          )}
        </div>
      )}
    </div>
  );
}

function addHtmlRepresentation(root) {
  const copy = { ...root };
  delete copy.clones;
  const json = JSON.stringify(copy, null, 2);
  root.htmlRepresentation = `<pre style="font-size: 11px">${json}</pre>`;

  for (const clone of root.clones) {
    addHtmlRepresentation(clone);
  }
}

interface ChartProps {
  data: unknown[];
}

function Chart({ data }: ChartProps): JSX.Element {
  useLayoutEffect(() => {
    const root = am5.Root.new("chartdiv");

    root.setThemes([am5themes_Animated.new(root)]);

    const container = root.container.children.push(
      am5.Container.new(root, {
        width: am5.percent(100),
        height: am5.percent(100),
        layout: root.verticalLayout,
      }),
    );

    const series = container.children.push(
      am5hierarchy.Tree.new(root, {
        valueField: "title",
        categoryField: "id",
        childDataField: "clones",
      }),
    );

    series.data.setAll(data);

    series.labels.template.setAll({ text: "{category}", fontSize: 12 });
    series.circles.template.setAll({ radius: 30 });
    series.nodes.template.setAll({
      toggleKey: "none",
      cursorOverStyle: "default",
      tooltipHTML: "<b>{title}</b>{htmlRepresentation}",
      showTooltipOn: "click",
    });

    return () => {
      root.dispose();
    };
  }, [data]);

  return <div id="chartdiv" style={{ width: "100vw", height: "100vh" }}></div>;
}
