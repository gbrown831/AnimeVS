import { Component, Output, EventEmitter, OnInit  } from '@angular/core';
import axios from 'axios';

@Component({
  selector: 'app-battle',
  standalone: true,
  imports: [],
  templateUrl: './battle.component.html',
  styleUrl: './battle.component.css'
})
export class BattleComponent {
  @Output() setView = new EventEmitter<boolean>();

  changeView(isHome: boolean) {
    this.setView.emit(isHome);
  }

  ngOnInit() {
    this.getImages();
  }

  getImages() {
    let character;
    axios.get('')
    .then((res) => {
      character = res.data.images[0]
    })
    .catch((err) => console.log(err));
  }
}
