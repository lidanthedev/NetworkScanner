import AccordionSummary from "@mui/material/AccordionSummary";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import Typography from "@mui/material/Typography";
import AccordionDetails from "@mui/material/AccordionDetails";
import Accordion from "@mui/material/Accordion";
import * as React from "react";

export interface AttackData {
  Attack_name: string,
  Date: string,
  IP: string,
  Is_Defended: boolean
  MAC: string,
  Time: string,
  WIFI: string,
}

type AttackAccordionProps = {
  attackData: AttackData,
  expanded: boolean,
  handleChange: (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => void,
  id: string
}

export default function AttackAccordion(props: AttackAccordionProps) {

  const attackData = props.attackData;

  return (
    <Accordion expanded={props.expanded} onChange={props.handleChange(`${props.id}`)}>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel1bh-content"
        id="panel1bh-header"
      >
        <Typography sx={{ width: '33%', flexShrink: 0 }}>
          {props.attackData.Attack_name}
        </Typography>
        <Typography sx={{ color: 'text.secondary' }}>
          {props.attackData.Date} {attackData.Time}
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Typography>
            Ip: {attackData.IP}
        </Typography>
        <Typography>
          Mac: {attackData.MAC}
        </Typography>
        <Typography>
          WIFI Name: {attackData.WIFI}
        </Typography>
        <Typography>
          Is Defended: {attackData.Is_Defended.toString()}
        </Typography>
      </AccordionDetails>
    </Accordion>
  )
}