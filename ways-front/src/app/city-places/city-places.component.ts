import { Component, OnInit } from '@angular/core';

import { CityPlacesService } from './city-places.service';
import { LinkData } from './link_data';

@Component({
  selector: 'app-city-places',
  templateUrl: './city-places.component.html',
  styleUrls: ['./city-places.component.css'],
  providers: [CityPlacesService]
})

export class CityPlacesComponent implements OnInit {

  data: LinkData;

  constructor(
    private cityPlacesService: CityPlacesService,
  ) { 
    this.cityPlacesService.link_data
      .subscribe(data => {
        this.data = data
        console.log(data.name)
      });
  }

  ngOnInit() {
    this.cityPlacesService.getLinkInfo();
  }

  // onStart(query: string) {
  //   this.query = query;
  // }

  // onStop() {
  //   console.log('stop');
  //   this.query = '';
  // }

}
