import React, { useEffect, useState } from 'react';
import { PieChart } from './PieChart';
import LineChart from './LineChart';
import { AttackData } from './AttackAccordion';

const Statistics: React.FC = () => {
    const [data, setData] = useState<{ name: string; value: number }[]>([]);

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

            

            setData(Object.entries(attackDict).map(([name, value]) => ({ name, value })));
        });
    }, []);

    return (
        <div>
            <PieChart width={600} height={600} data={data} />
        </div>
    );
};

export default Statistics;