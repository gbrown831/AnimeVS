import { Component, Output, EventEmitter, OnInit  } from '@angular/core';
import axios from 'axios';
import {NgbCollapseModule} from '@ng-bootstrap/ng-bootstrap';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import {
  trigger,
  state,
  style,
  animate,
  transition,
} from '@angular/animations';


@Component({
  selector: 'app-battle',
  standalone: true,
  imports: [NgbCollapseModule],
  templateUrl: './battle.component.html',  
  styleUrl: './battle.component.css',
  animations: [
    trigger('fadeImage', [
      state('hasWon', style({
        opacity: 1,
      })),
      state('hasLost', style({
        opacity: 0.6,
      })),
      transition('hasWon => hasLost', [
        animate('1s')
      ]),
    ])
  ]
})

export class BattleComponent {
  @Output() setView = new EventEmitter<boolean>();
  leftURL!: string;
  rightURL!: string;
  left_char: any = {};
  right_char: any = {};
  leftVotes!: string | number;
  rightVotes!: string | number;

  hasVoted: boolean = false;

  left_percentage!: string;
  right_percentage!: string;

  fadeLeft = this.hasVoted && (this.leftVotes < this.rightVotes);
  fadeRight = this.hasVoted && (this.leftVotes > this.rightVotes);


  changeView(isHome: boolean) {
    this.setView.emit(isHome);
  }

  ngOnInit() {
    this.getImages();
  }

  getImages() {
    axios.get('http://127.0.0.1:5000/')
    .then((res) => {
      this.leftURL = res.data.char1_url[0]
      this.rightURL = res.data.char2_url[0]
      this.left_char = res.data.char1;
      this.right_char = res.data.char2;
      console.log(res.data)

      this.hasVoted = false;
    })
    .catch((err) => console.log(err));
  }


  postVotes(id: string | number) {

    this.hasVoted = true;
    axios.post('http://127.0.0.1:5000/', {
      "char1_id": this.left_char.id,
      "char2_id": this.right_char.id,
      "winner": id
    })
    .then((res) => {
      if (res.data.switch) {
        this.leftVotes = (res.data.votes2 * 100) / (res.data.votes1 + res.data.votes2);
        this.rightVotes = (res.data.votes1 * 100) / (res.data.votes1 + res.data.votes2);
      } else {
        this.leftVotes = (res.data.votes1 * 100) / (res.data.votes1 + res.data.votes2);
        this.rightVotes = (res.data.votes2 * 100) / (res.data.votes1 + res.data.votes2);
      }

      this.fadeLeft = (this.leftVotes < this.rightVotes);
      this.fadeRight = (this.leftVotes > this.rightVotes);
      console.log(this.fadeLeft, this.fadeRight)

      this.left_percentage = Math.floor((this.leftVotes / 100) * 80).toString() + 'vw';
      this.right_percentage = Math.floor((this.rightVotes / 100) * 80).toString() + 'vw';

      this.leftVotes = Math.floor(this.leftVotes).toString() + '%'
      this.rightVotes = Math.floor(this.rightVotes).toString() + '%'
    })
    .catch((err) => console.log(err));

    setTimeout(() => {
      this.getImages();
    }, 3000);
  }
}
