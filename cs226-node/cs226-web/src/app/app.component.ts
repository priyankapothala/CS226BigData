import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { AppService } from './app.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  params: any = {
    criteria: 'quality_of_life'
  };
  records:any = [];
  criteriaList: Array<any> = [{ name: 'Quality of Life', value: 'quality_of_life' }, 
  { name: 'Pollution', value: 'pollution_index' }, 
  { name: 'Crime', value: 'crime_index' }, 
  { name: 'Population', value: 'population'},
  {name:'Safety',value:'safety_index'},
  {name:'Healthcare',value:'health_care_index'}]
  constructor(private appService: AppService, private route: ActivatedRoute,private router:Router) { }

  getRanking(params) {
    this.appService.getCities(params).subscribe((response: any) => {
      this.records = response;
    }, (err) => {
      console.log(err);
    })
  }
  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.params.criteria = params['criteria'] || 'quality_of_life';
      this.getRanking(this.params);
    })
  }
}
