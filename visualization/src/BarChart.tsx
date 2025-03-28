import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface DataPoint {
  tagOrder: string;
  count: number;
}

interface BarChartProps {
  data: DataPoint[];
}

const BarChart: React.FC<BarChartProps> = ({ data }) => {
  const ref = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    if (data.length === 0) return;

    const svg = d3.select(ref.current);
    const width = 500;
    const height = 300;
    const margin = { top: 20, right: 30, bottom: 40, left: 40 };

    const x = d3
      .scaleBand()
      .domain(data.map(d => d.tagOrder))
      .range([margin.left, width - margin.right])
      .padding(0.1);

    const y = d3
      .scaleLinear()
      .domain([0, d3.max(data, d => d.count) as number])
      .nice()
      .range([height - margin.bottom, margin.top]);

    svg.selectAll('*').remove();

    svg
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('style', 'max-width: 100%; height: auto;');

    svg
      .append('g')
      .attr('fill', 'steelblue')
      .selectAll('rect')
      .data(data)
      .join('rect')
      .attr('x', d => x(d.tagOrder) as number)
      .attr('y', d => y(d.count))
      .attr('height', d => y(0) - y(d.count))
      .attr('width', x.bandwidth());

    svg
      .append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x));

    svg
      .append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));
  }, [data]);

  return <svg ref={ref}></svg>;
};

export default BarChart;

