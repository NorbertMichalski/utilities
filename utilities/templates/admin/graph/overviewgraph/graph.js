var chart;
jQuery(document).ready(function() {
	chart = new Highcharts.Chart({
		chart: {
			renderTo: 'chart_container',
			defaultSeriesType: 'line',
			marginRight: 130,
			marginBottom: 30,
		},
		title: {
			text: 'MROsupply statistics ',
			x: -20,
		},
		subtitle: {
			text: '',
			x: -20
		},
		xAxis: {
			dates: dates,
		},
		yAxis: {
			title: {
				text: 'Values'
			},
			plotLines: [{
				value: 0,
				width: 1,
				color: '#808080'
			}]
		},
		tooltip: {
			formatter: function() {
	                return ''+ this.series.name +''+this.x +': '+ this.y;
			}
		},
		legend: {
			layout: 'vertical',
			align: 'right',
			verticalAlign: 'top',
			x: -10,
			y: 100,
			borderWidth: 0
		},
		series: [{
			name: 'price',
			data: prices,
		}, {
			name: 'sales',
			data: sales,
		}, {
			name: 'rank',
			data: ranks,
		}, {
			name: 'visits',
			data: visits,
		}]
	});
});