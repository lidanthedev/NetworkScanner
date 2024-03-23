import React, { useEffect, useState } from 'react';
import { PieChart } from './PieChart';
import LineChart from './LineChart';
import { AttackData } from './AttackAccordion';

const Statistics: React.FC = () => {
    const [data, setData] = useState<{ name: string; value: number }[]>([]);
    const [timedData, setTimedData] = useState<{ x: number; y: number }[]>([]);

    const getAttacks = () => {
        return fetch('http://localhost:5000/getAttacks').then(response => response.json());
    }
    useEffect(() => {


        getAttacks().then((attacks: AttackData[]) => {
            const attackDict: { [key: string]: number } = {};

            for (const item of attacks) {
                const attackName = item.Attack_name;
                if (attackName in attackDict) {
                    attackDict[attackName] += 1;
                } else {
                    attackDict[attackName] = 1;
                }
            }

            const attacksByHour: { [key: string]: number } = {};
            for (const item of attacks) {
                const attackTime = item.Time;
                const [day, month, year] = item.Date.split('/');
                const [hour, minute, second] = attackTime.split(':');
                const attackDate = new Date(parseInt(year), parseInt(month) - 1, parseInt(day), parseInt(hour), parseInt(minute), parseInt(second));
                const key = attackDate.toISOString().slice(0, 13); // Get the date and hour in YYYY-MM-DDTHH format
                if (key in attacksByHour) {
                    attacksByHour[key] += 1;
                } else {
                    attacksByHour[key] = 1;
                }
            }
            const hourlyData: { x: number; y: number }[] = Object.entries(attacksByHour).map(([x, y]) => ({ x: parseInt(x.split("-")[2]) + parseInt(x.split("T")[1]), y }));
            hourlyData.sort((a, b) => a.x - b.x);
            setTimedData(hourlyData);

            setData(Object.entries(attackDict).map(([name, value]) => ({ name, value })));
        });
    }, []);

    return (
        <div>
            <PieChart width={600} height={600} data={data} />
            <LineChart width={600} height={600} data={timedData} />
        </div>
    );
};

export default Statistics;