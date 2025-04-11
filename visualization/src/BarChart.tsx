import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export interface DataPoint {
  tagOrder: string;
  count: number;
}

interface BarChartProps {
  data: DataPoint[];
  message: string;
}


// @ts-ignore
const BarChart: React.FC<BarChartProps> = ({ data, message}) => {
  const ref = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    if (data.length === 0) return;

    const svg = d3.select(ref.current);
    const width = 600;
    const height = 300;
    const margin = { top: 20, right: 30, bottom: 40, left: 60 };

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
      .attr('fill', '#535bf2')
      .attr('hover', '#646cff')
      .selectAll('rect')
      .data(data)
      .join('rect')
      .attr('x', d => x(d.tagOrder) as number)
      .attr('y', d => y(d.count))
      .attr('height', d => y(0) - y(d.count))
      .attr('width', x.bandwidth())
      .on('mouseover', function (){
        d3.select(this).attr('fill', '#646cff');
      })
      .on('mouseout', function(){
        d3.select(this).attr('fill', '#535bf2');
      });

    svg
      .append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x));

    svg
      .append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

    svg.append("text")
        .attr("class", "x label")
        .attr("text-anchor", "end")
        .attr("x", width/2 + 45)
        .attr("y", height - 6)
        .text("Location");

    svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "middle")
        .attr("x", -height / 2)
        .attr("y", 2)
        .attr("dy", ".55em")
        .attr("transform", "rotate(-90)")
        .text(message);
  }, [data]);

  return <svg ref={ref}></svg>;
};

export default BarChart;

